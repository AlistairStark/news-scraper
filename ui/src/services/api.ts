import Axios from "axios";
import { ApiRoutes, AppRoutes } from "../types";
import { toast } from "react-toastify";

const TOKEN = "token";

export const axios = Axios.create({
  baseURL: "",
});

function getMessage(error: any) {
  if (error?.response?.data?.message) {
    return error?.response?.data?.message;
  }
  return "Something went wrong...";
}

axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (401 === error?.response?.status) {
      localStorage.removeItem(TOKEN);
      window.location.href = AppRoutes.Login;
    } else if (400 === error?.response?.status) {
      console.log(error.response.data);
      toast.error(getMessage(error));
    } else {
      toast.error(getMessage(error));
    }
  }
);

export function initAxios() {
  const token: string | null = localStorage.getItem(TOKEN);
  if (token) {
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  }
}

function setAuth(token: string) {
  localStorage.setItem(TOKEN, token);
  initAxios();
}

export async function login(
  email: string,
  password: string
): Promise<void | { message: string }> {
  try {
    const res = await axios.post<{ token: string }>(ApiRoutes.UserLogin, {
      email,
      password,
    });
    setAuth(res.data.token);
  } catch (e: any) {
    return e?.response?.data || { message: "error logging in" };
  }
}

export function isAuthenticated(): boolean {
  return !!localStorage.getItem(TOKEN);
}

export function removeToken() {
  localStorage.removeItem(TOKEN);
}
