import { JobPostForm } from "./JobPostForm";

function JobPost() {
  return (
    <>
      <h1 className="w-full text-center text-3xl font-bold py-10 bg-gray-50">
        You can publish a new position here.
      </h1>
      <div className=" bg-gray-50  pb-10">
        <div className="w-9/12 flex flex-col mx-auto">
          <JobPostForm />
        </div>
      </div>
    </>
  );
}

export default JobPost;