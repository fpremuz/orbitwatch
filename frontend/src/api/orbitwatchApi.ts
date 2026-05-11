import axios from "axios"

export const orbitwatchApi = axios.create({
  baseURL: "http://localhost:8000",
})