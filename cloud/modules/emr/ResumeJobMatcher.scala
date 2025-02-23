/*
 * ResumeJobMatcherWithCleaning.scala
 * ------------------------------------------------------------------
 * A more scalable Spark job to match resumes to jobs by shared skills,
 * including a basic data-cleaning process.
 *
 * MAJOR STEPS:
 *   0. Basic Data Cleaning for jobs and resumes.
 *   1. Extract skills from job descriptions and resumes.
 *   2. Explode each skill into a separate row (inverted index).
 *   3. Join on the skill to find potential matches (avoids cross-join).
 *   4. Calculate match scores (e.g., matched_skill_count / job_skill_count).
 *   5. Rank the top-N matching jobs for each resume.
 *   6. Save results to S3 in CSV format.
 *
 * REQUIREMENTS:
 *   - Spark on EMR (or any Hadoop cluster)
 *   - S3 read/write permissions (IAM role or credentials)
 *   - Scala 2.12.x or compatible
 *   - Properly formatted CSV input files
 *
 * USAGE (Spark Shell Example):
 *   1) spark-shell --deploy-mode cluster --executor-memory 4G \
 *        --executor-cores 2 --num-executors 3
 *   2) Paste this script into the Spark shell (or split into logical steps).
 *   3) Update s3://MY-BUCKET paths below before running.
 */

import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions.Window

// -----------------------------------------------------------------------------
// 1. Initialize Spark Session
// -----------------------------------------------------------------------------
val spark = SparkSession.builder()
  .appName("ResumeJobMatcherWithCleaning")
  .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

// -----------------------------------------------------------------------------
// 2. Define Input Paths & Parameters (Update These)
// -----------------------------------------------------------------------------
val jobsPath    = "s3://MY-BUCKET/jobs/jobs_table.csv"       // CHANGE
val resumesPath = "s3://MY-BUCKET/resumes/Resume.csv"         // CHANGE
val outputPath  = "s3://MY-BUCKET/output/matched_results_v2"  // CHANGE
val topN        = 5   // Number of top matches per resume

// -----------------------------------------------------------------------------
// 3. Read the Raw CSV Files from S3
// -----------------------------------------------------------------------------
val rawJobsDF = spark.read
  .option("header", "true")
  .option("inferSchema", "true")
  .csv(jobsPath)

val rawResumesDF = spark.read
  .option("header", "true")
  .option("inferSchema", "true")
  .csv(resumesPath)

println("=== Raw Job Data Schema ===")
rawJobsDF.printSchema()
println("=== Raw Resume Data Schema ===")
rawResumesDF.printSchema()

// -----------------------------------------------------------------------------
// 4. Basic Data Cleaning for Jobs & Resumes
// -----------------------------------------------------------------------------
// This is a minimal example. Adjust as needed for your real data.
//
// Steps we demonstrate here (you can add more if needed):
//  - Drop rows missing required columns (like job id, resume id, or text fields).
//  - Drop duplicates based on ID columns (e.g. job_id, resume_id).
//  - Trim leading/trailing whitespace in critical fields.
//  - (Optional) Fill null values with some placeholder to avoid errors.

//
// 4.1 Clean Jobs
//
val jobsDF = rawJobsDF
  .filter(col("id").isNotNull && col("description").isNotNull)     // Must have job ID + description
  .dropDuplicates("id")                                            // Drop duplicate job IDs
  .withColumn("id", trim(col("id")))
  .withColumn("title", trim(col("title")))
  .withColumn("description", trim(col("description")))
  // Optionally fill null with "Unknown" or some fallback
  .na.fill("Unknown", Seq("title"))
  // Repeat for other columns as needed

//
// 4.2 Clean Resumes
//
val resumesDF = rawResumesDF
  .filter(col("ID").isNotNull && col("Resume_str").isNotNull)      // Must have resume ID + text
  .dropDuplicates("ID")                                            // Drop duplicate resume IDs
  .withColumn("ID", trim(col("ID")))
  .withColumn("Resume_str", trim(col("Resume_str")))
  // Optionally fill null with "Unknown" in other columns
  // .na.fill("Unknown", Seq("some_other_column"))

// Sanity check: show some cleaned records
println("=== Cleaned Jobs (sample) ===")
jobsDF.show(5, truncate = false)
println("=== Cleaned Resumes (sample) ===")
resumesDF.show(5, truncate = false)

// -----------------------------------------------------------------------------
// 5. Define Skill Extraction (Simple UDF with a Fixed Skill List)
// -----------------------------------------------------------------------------
val skillList = List("scala", "spark", "aws", "java", "python", "hadoop", "sql", "linux")

val extractSkillsUDF = udf((text: String) => {
  if (text == null) Seq.empty[String]
  else {
    // Lowercase the text
    val lowerText = text.toLowerCase
    // Filter to only known skills
    skillList.filter(skill => lowerText.contains(skill))
  }
})

val jobsWithSkills = jobsDF.withColumn("job_skills", extractSkillsUDF(col("description")))
val resumesWithSkills = resumesDF.withColumn("resume_skills", extractSkillsUDF(col("Resume_str")))

// -----------------------------------------------------------------------------
// 6. Explode Skills to Create a Skill-Based "Inverted Index"
// -----------------------------------------------------------------------------
// This approach is more scalable than a cross-join.
//
// We'll produce two DataFrames:
//
// explodedJobs:    (job_id, title, skill, job_skills)
// explodedResumes: (resume_id, skill, resume_skills)
//
val explodedJobs = jobsWithSkills
  .withColumn("skill", explode(col("job_skills")))
  .select(
    col("id").alias("job_id"),
    col("title"),
    col("skill"),
    col("job_skills") // Keep the full array if we want to see all skills
  )

val explodedResumes = resumesWithSkills
  .withColumn("skill", explode(col("resume_skills")))
  .select(
    col("ID").alias("resume_id"),
    col("skill"),
    col("resume_skills")
  )

// -----------------------------------------------------------------------------
// 7. Join on Skill to Find Potential Matches
// -----------------------------------------------------------------------------
val matchedBySkillDF = explodedResumes.join(explodedJobs, Seq("skill"))

// -----------------------------------------------------------------------------
// 8. Aggregate Matched Skills per (resume_id, job_id)
// -----------------------------------------------------------------------------
val aggregatedMatches = matchedBySkillDF
  .groupBy("resume_id", "job_id")
  .agg(
    collect_set("skill").as("matched_skills"),
    first("resume_skills").as("resume_skills"),
    first("job_skills").as("job_skills"),
    first("title").as("title")
  )
  .withColumn("matched_skill_count", size(col("matched_skills")))
  .withColumn("job_skill_count", size(col("job_skills")))
  .withColumn("resume_skill_count", size(col("resume_skills")))

// -----------------------------------------------------------------------------
// 9. Calculate a Match Score
// -----------------------------------------------------------------------------
// Example: match_score = matched_skill_count / job_skill_count
// or you can do Jaccard: matched_skill_count / size(array_union(...))
val scoredDF = aggregatedMatches
  .withColumn("match_score",
    when(col("job_skill_count") === 0, lit(0)) // avoid div by zero
      .otherwise(col("matched_skill_count") / col("job_skill_count").cast("double"))
  )
  .filter(col("matched_skill_count") > 0)  // keep only matches

// -----------------------------------------------------------------------------
// 10. Rank Jobs per Resume & Keep Top N
// -----------------------------------------------------------------------------
val w = Window.partitionBy("resume_id").orderBy(col("match_score").desc, col("matched_skill_count").desc)

val rankedDF = scoredDF
  .withColumn("rn", row_number().over(w))
  .filter(col("rn") <= topN)
  .drop("rn")

// -----------------------------------------------------------------------------
// 11. Select Final Columns & Show Output
// -----------------------------------------------------------------------------
println(s"=== Showing Top $topN Matches per Resume ===")
val finalDF = rankedDF.select(
  col("resume_id"),
  col("resume_skills"),
  col("job_id"),
  col("title"),
  col("job_skills"),
  col("matched_skills"),
  col("matched_skill_count"),
  col("job_skill_count"),
  col("resume_skill_count"),
  col("match_score")
)

finalDF.show(50, truncate = false)

// -----------------------------------------------------------------------------
// 12. Write Results to S3
// -----------------------------------------------------------------------------
finalDF.write
  .mode("overwrite")
  .option("header", "true")
  .csv(outputPath)

println(s"Top-$topN matched results saved to: $outputPath")

// -----------------------------------------------------------------------------
// 13. Stop Spark Session
// -----------------------------------------------------------------------------
spark.stop()
