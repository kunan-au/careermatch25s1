import { useMutation, useQueryClient } from "@tanstack/react-query";
//import axios from "axios";
import toast from "react-hot-toast";
//import { api } from "@/services/api";

// Original type definitions
/*
type SuccessResumeResponse = {
  message: string;
  fileUrl: string;
};

type ResumeResponse = SuccessResumeResponse | undefined;
*/

// Updated type definitions
type SuccessResumeResponse = {
  message: string;
  fileUrl: string;
};

type ResumeResponse = SuccessResumeResponse | undefined;

// Original upload function
/*
const uploadResume = async (
  email: string,
  file: File
): Promise<ResumeResponse> => {
  // 创建本地文件URL
  const fileUrl = URL.createObjectURL(file);
  
  // 模拟成功响应
  return {
    message: `Resume for ${email} uploaded successfully`,
    fileUrl: fileUrl
  };
};
*/

// Updated upload function with validation
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const SUPPORTED_FORMATS = {
  'application/pdf': ['.pdf'],
  'application/msword': ['.doc'],
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
  'text/plain': ['.txt']
};

const validateFile = (file: File): string | null => {
  // 检查文件大小
  if (file.size > MAX_FILE_SIZE) {
    return `File size should not exceed ${MAX_FILE_SIZE / (1024 * 1024)}MB`;
  }

  // 检查文件类型
  if (!Object.keys(SUPPORTED_FORMATS).includes(file.type)) {
    return 'File format not supported. Please upload PDF, DOC, DOCX, or TXT files.';
  }

  return null;
};

const uploadResume = async (
  email: string,
  file: File
): Promise<ResumeResponse> => {
  // 文件验证
  const validationError = validateFile(file);
  if (validationError) {
    throw new Error(validationError);
  }

  try {
    // 创建本地文件URL
    const fileUrl = URL.createObjectURL(file);
    
    return {
      message: `Resume for ${email} uploaded successfully`,
      fileUrl: fileUrl
    };
  } catch (error) {
    throw new Error('Failed to process the file. Please try again.');
  }
};

export function useResumeUpdate() {
  const queryClient = useQueryClient();
  const {
    mutateAsync: updateResume,
    status,
    data: responseData,
  } = useMutation<ResumeResponse, Error, { email: string; file: File }>({
    mutationFn: ({ email, file }) => uploadResume(email, file),
    onSuccess: (data) => {
      toast.success("Resume uploaded successfully!");
      queryClient.setQueryData(["profile", data?.message.split(" ")[2]], (oldData: any) => ({
        ...oldData,
        resume: data?.fileUrl
      }));
    },
    onError: (err) => {
      toast.error(err.message);
    },
  });

  return { status, updateResume, responseData };
}
