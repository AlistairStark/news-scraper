import Axios from "axios";
import { ApiRoutes, AppRoutes } from "../types";

const TOKEN = "token";

export const axios = Axios.create({
  baseURL: "",
});

axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (401 === error?.response?.status) {
      localStorage.removeItem(TOKEN);
      window.location.href = AppRoutes.Login;
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
