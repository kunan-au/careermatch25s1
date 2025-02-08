import React, { useCallback, useState } from "react";
import { Button } from "@/components/ui/button";
import { useUser } from "../SignIn/useUser";
import { useProfile } from "../ProfileInfo/useProfile";
import { useResumeUpdate } from "../ProfileInfo/useResumeUpdate";

const defaultInfoData = {
  email: "string",
  name: "string",
  avatar: "string",
  resume: "string",
};

function HomePage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);

  const { user_profile } = useUser();
  const { email } = user_profile ? user_profile : { email: "user@example.com" };

  const { user_info } = useProfile(email);
  const { name } = user_info ? user_info : defaultInfoData;

  const { updateResume } = useResumeUpdate();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files?.length) {
      setSelectedFile(event.target.files[0]);
      console.log(event.target.files[0]);
    } else {
      setSelectedFile(null);
    }
  };

  const handleUpload = async () => {
    if (selectedFile) {
      console.log("Uploading", selectedFile.name);
      await updateResume({ email, file: selectedFile });

      // Upload File Interface
      setSelectedFile(null);
    }
  };

  const handleDragOver = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      setIsDragOver(true);
    },
    []
  );

  const handleDragLeave = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      setIsDragOver(false);
    },
    []
  );

  const handleDrop = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(false);

    const files = event.dataTransfer.files;
    if (files.length) {
      // Process the files here
      setSelectedFile(files[0]);
      console.log(files[0]);
    } else {
      setSelectedFile(null);
    }
  }, []);

  return (
    <div className="flex flex-col items-center justify-center gap-5 bg-gray-5 my-16">
      <h2 className="w-full text-center text-3xl font-bold">
        Hello, {name ? name : "Anonymous"}.
      </h2>
      <h1 className="w-full text-center text-3xl font-bold mb-5">
        Welcome to CareerMatch, where your perfect job match begins.
      </h1>
      <h2 className="text-md text-center font-bold text-primary">
        Please upload your resume and let us embark on a tailor-made career
        journey for you.
      </h2>
      <div
        className={`border-2 ${
          isDragOver ? "border-blue-500" : "border-gray-300"
        } border-dashed rounded-md bg-white h-64 w-96 flex flex-col justify-center items-center cursor-pointer text-center`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <p className="text-gray-500">
          You can drag your file here or select it using the button below.
        </p>
      </div>
      <div>
        <input
          id="fileInput"
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          style={{ display: "none" }} // Hide real file input
        />
        <div className="button-group flex gap-10">
          <Button
            className="choose-file-button"
            onClick={() => document.getElementById("fileInput")?.click()}
          >
            CHOOSE FILE
          </Button>
          <Button
            className="upload-button"
            onClick={handleUpload}
            disabled={!selectedFile}
          >
            UPLOAD FILE
          </Button>
        </div>
        {selectedFile && (
          <div className="file-details">Selected file: {selectedFile.name}</div>
        )}
      </div>
    </div>
  );
} // End HomePage

export default HomePage;
