import { useAuthStore } from "./auth";

const FE_BASE = "/api/v1";
const IAM_BASE = "/iam/api/v1";

async function request<T>(
  path: string,
  options: RequestInit = {},
  base: string = FE_BASE
): Promise<T> {
  const token = useAuthStore.getState().accessToken;
  const headers: HeadersInit = {
    ...(options.headers || {}),
  };
  if (!(options.body instanceof URLSearchParams)) {
    (headers as Record<string, string>)["Content-Type"] = "application/json";
  }
  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${base}${path}`, { ...options, headers });

  if (res.status === 401) {
    useAuthStore.getState().logout();
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || res.statusText);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: "POST", body: JSON.stringify(body) }),
  patch: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: "PATCH", body: JSON.stringify(body) }),
  delete: (path: string) => request<void>(path, { method: "DELETE" }),
};

export async function iamRegister(email: string, fullName?: string) {
  return request<{ id: string; email: string }>(
    "/auth/register",
    {
      method: "POST",
      body: JSON.stringify({ email, full_name: fullName }),
    },
    IAM_BASE
  );
}

export async function iamRequestOtp(email: string) {
  return request<{ message: string; dev_otp?: string }>(
    `/auth/request-otp?email=${encodeURIComponent(email)}`,
    { method: "POST" },
    IAM_BASE
  );
}

export async function iamVerifyOtp(email: string, otp: string) {
  return request<{ access_token: string; token_type: string; apps: string[] }>(
    `/auth/verify-otp?email=${encodeURIComponent(email)}&otp=${encodeURIComponent(otp)}`,
    { method: "POST" },
    IAM_BASE
  );
}
