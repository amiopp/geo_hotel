import { buildFallbackAnalysis, hotels as fallbackHotels } from "./sampleData";
import type { Hotel, HotelAnalysis } from "./types";

function resolveApiBaseUrl(): string {
  const configuredUrl = import.meta.env.VITE_API_BASE_URL;
  if (typeof window === "undefined") {
    return configuredUrl ?? "http://localhost:8008";
  }

  const pageHostname = window.location.hostname;
  const pageIsLoopback = pageHostname === "localhost" || pageHostname === "127.0.0.1";
  if (configuredUrl) {
    try {
      const parsedUrl = new URL(configuredUrl);
      const apiIsLoopback = parsedUrl.hostname === "localhost" || parsedUrl.hostname === "127.0.0.1";
      if (apiIsLoopback && !pageIsLoopback) {
        parsedUrl.hostname = pageHostname;
        parsedUrl.protocol = window.location.protocol;
        return parsedUrl.origin;
      }
    } catch {
      return configuredUrl;
    }
    return configuredUrl;
  }

  return `${window.location.protocol}//${pageHostname}:8008`;
}

const API_BASE_URL = resolveApiBaseUrl();

export type LoginResponse = {
  access_token: string;
  token_type: string;
  user_name: string;
};

export async function loginUser(identifier: string, password: string): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE_URL}/api/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ identifier, password }),
  });

  if (!response.ok) {
    let message = "Identifiant ou mot de passe incorrect";
    try {
      const payload = await response.json();
      if (typeof payload.detail === "string") {
        message = payload.detail;
      }
    } catch {
      message = "Connexion impossible pour le moment";
    }
    throw new Error(message);
  }

  return response.json();
}

function authHeaders(token?: string): HeadersInit {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function fetchHotels(token?: string): Promise<Hotel[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/hotels`, { headers: authHeaders(token) });
    if (!response.ok) {
      throw new Error("API unavailable");
    }
    return response.json();
  } catch {
    return fallbackHotels;
  }
}

export async function fetchAnalysis(hotelId: number, radiusM: number, token?: string): Promise<HotelAnalysis> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/hotels/${hotelId}/analysis?radius_m=${radiusM}`, {
      headers: authHeaders(token),
    });
    if (!response.ok) {
      throw new Error("API unavailable");
    }
    return response.json();
  } catch {
    return buildFallbackAnalysis(hotelId, radiusM);
  }
}
