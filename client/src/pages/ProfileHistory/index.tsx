import { useState } from "react";

export default function ProfileHistory() {
    /*A page for history */
    const [hoveredJob, setHoveredJob] = useState<string | null>(null);

    const jobDetails = {
        "Frontend Developer at TechCorp": "TechCorp is a leading tech company specializing in web development. This role involves building responsive user interfaces.",
        "UX Designer at CreateLab": "CreateLab focuses on innovative design solutions. This role includes user research and creating wireframes.",
        "Software Engineer at DevSolutions": "DevSolutions is a software consultancy. This role involves backend development and cloud integration.",
    };

    return (
        <div className="text-center bg-gray-50">
            <h1 className="w-full text-center text-3xl font-bold py-10">
                Your Application History
            </h1>
            <ul className="space-y-4 max-w-4xl mx-auto text-left">
                {Object.keys(jobDetails).map((jobTitle) => (
                    <li
                        key={jobTitle}
                        className="bg-white shadow rounded-lg p-6 border relative"
                        onMouseEnter={() => setHoveredJob(jobTitle)}
                        onMouseLeave={() => setHoveredJob(null)}
                    >
                        <div className="flex justify-between items-center">
                            <div>
                                <h3 className="font-bold mt-px">{jobTitle}</h3>
                                <p className="text-sm text-gray-500">
                                    {jobTitle === "Frontend Developer at TechCorp"
                                        ? "Applied on March 25, 2025"
                                        : jobTitle === "UX Designer at CreateLab"
                                        ? "Applied on February 12, 2025"
                                        : "Applied on January 30, 2025"}
                                </p>
                            </div>
                            <span
                                className={`text-sm font-medium px-3 py-1 rounded-full ${
                                    jobTitle === "Frontend Developer at TechCorp"
                                        ? "text-green-600 bg-green-100"
                                        : jobTitle === "UX Designer at CreateLab"
                                        ? "text-red-600 bg-red-100"
                                        : "text-blue-600 bg-blue-100"
                                }`}
                            >
                                {jobTitle === "Frontend Developer at TechCorp"
                                    ? "Under Review"
                                    : jobTitle === "UX Designer at CreateLab"
                                    ? "Rejected"
                                    : "Interview Scheduled"}
                            </span>
                        </div>
                        {hoveredJob === jobTitle && (
                            <div className="absolute top-1/2 left-full ml-4 transform -translate-y-1/2 w-64 bg-gray-100 shadow-lg rounded-lg p-4 text-sm text-gray-700">
                                {jobDetails[jobTitle]}
                            </div>
                        )}
                    </li>
                ))}
            </ul>
            <br />
        </div>
    );
}
