import React, { useCallback, useState, useEffect } from "react";
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
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);

  const { user_profile } = useUser();
  const { email } = user_profile ? user_profile : { email: "user@example.com" };

  const { user_info } = useProfile(email);
  const { name } = user_info ? user_info : defaultInfoData;

  const { updateResume } = useResumeUpdate();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files?.length) {
      const file = event.target.files[0];
      if (file.type === "application/pdf") {
        setSelectedFile(file);
        setPreviewUrl(URL.createObjectURL(file));
        console.log("Selected file:", file);
      } else {
        alert("Please upload a PDF file.");
        setSelectedFile(null);
        setPreviewUrl(null);
      }
    }
  };

  const confirmUpload = async () => {
    if (selectedFile) {
      console.log("Uploading", selectedFile.name);
      // 调用 updateResume(selectedFile) 可在此处集成上传逻辑
      setSelectedFile(null);
      setPreviewUrl(null);
    }
    setShowConfirmDialog(false);
  };

  const cancelUpload = () => {
    setShowConfirmDialog(false);
  };

  const handleDeleteFile = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    console.log("File selection cleared");
  };

  const handleChooseFile = () => {
    const input = document.getElementById("fileInput") as HTMLInputElement;
    if (input) {
      input.value = "";
      input.click();
    }
  };

  const handleDragOver = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(false);

    const files = event.dataTransfer.files;
    if (files.length && files[0].type === "application/pdf") {
      setSelectedFile(files[0]);
      setPreviewUrl(URL.createObjectURL(files[0]));
      console.log("Dropped file:", files[0]);
    } else {
      alert("Please upload a PDF file.");
      setSelectedFile(null);
      setPreviewUrl(null);
    }
  }, []);

  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  return (
    <div className="flex flex-col items-center justify-center gap-5 bg-gray-5 my-16">
      <h2 className="w-full text-center text-3xl font-bold">Hello, {name || "Anonymous"}.</h2>
      <h1 className="w-full text-center text-3xl font-bold mb-5">
        Welcome to CareerMatch, where your perfect job match begins.
      </h1>
      <h2 className="text-md text-center font-bold text-primary">
        Please upload your resume and let us embark on a tailor-made career journey for you.
      </h2>

      <div
        className={`border-2 ${isDragOver ? "border-blue-500" : "border-gray-300"} border-dashed rounded-md bg-white h-64 w-96 flex flex-col justify-center items-center cursor-pointer text-center`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <p className="text-gray-500">You can drag your file here or select it using the button below.</p>
      </div>

      <div>
        <input id="fileInput" type="file" accept=".pdf" onChange={handleFileChange} style={{ display: "none" }} />
        <div className="button-group flex gap-5 mt-3">
          <Button onClick={handleChooseFile}>
            CHOOSE FILE
          </Button>
          {selectedFile && (
            <Button className="bg-red-500 text-white" onClick={handleDeleteFile}>
              DELETE FILE
            </Button>
          )}
          <Button onClick={() => setShowConfirmDialog(true)} disabled={!selectedFile}>
            UPLOAD FILE
          </Button>
        </div>
        {selectedFile && <div className="text-gray-700 mt-2">Selected file: {selectedFile.name}</div>}
      </div>

      {previewUrl && (
        <div className="mt-5 w-full max-w-2xl">
          <h2 className="text-xl font-bold mb-3">Resume Preview</h2>
          <iframe src={previewUrl} width="100%" height="500px" style={{ border: "1px solid #ccc" }} title="Resume Preview" />
        </div>
      )}

      {showConfirmDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-80">
            <h2 className="text-lg font-bold mb-4">Confirm Upload</h2>
            <p className="text-gray-600 mb-6">
              Are you sure you want to upload this resume?
            </p>
            <div className="flex justify-end gap-4">
              <button
                onClick={cancelUpload}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
              >
                Cancel
              </button>
              <button
                onClick={confirmUpload}
                className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default HomePage;
