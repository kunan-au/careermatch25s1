import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:16000",
  withCredentials: true,
  headers: {
    Accept: "application/json",
  },
});
