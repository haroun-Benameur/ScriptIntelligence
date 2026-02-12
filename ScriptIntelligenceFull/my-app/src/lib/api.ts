const API_BASE = import.meta.env.VITE_API_URL || "/api";

const FETCH_TIMEOUT = 60000;

async function fetchWithTimeout(url: string, options?: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), FETCH_TIMEOUT);
  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    return res;
  } catch (e) {
    if (e instanceof Error && e.name === "AbortError") {
      throw new Error("Délai dépassé. Vérifiez que le backend tourne sur http://127.0.0.1:8000");
    }
    throw e;
  } finally {
    clearTimeout(timeout);
  }
}

async function fetchApi<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetchWithTimeout(`${API_BASE}${url}`, {
    ...options,
    headers: { ...options?.headers },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(typeof err.detail === "string" ? err.detail : JSON.stringify(err.detail));
  }
  return res.json();
}

export interface TestCase {
  requirement_id: string;
  test_name: string;
  description: string;
  inputs: Record<string, unknown>;
  expected_output: string;
}

export interface AnalyzeResponse {
  drift_detected: boolean;
  changes?: {
    added: { requirement_id: string }[];
    updated: { requirement_id: string }[];
    removed: { requirement_id: string }[];
  };
}

export interface GenerateResponse {
  status: string;
  requirements_count: number;
  generated_tests_count: number;
  generated_tests: TestCase[];
  reports: { test_generation_report: string };
}

export interface RegenerateResponse {
  status: string;
  generated_tests_count: number;
  total_tests: number;
  generated_tests: TestCase[];
  reports: { test_generation_report: string; drift_report: string };
}

export const api = {
  async uploadFsd(file: File): Promise<{ status: string; filename: string }> {
    const form = new FormData();
    form.append("file", file);
    const res = await fetchWithTimeout(`${API_BASE}/upload-fsd`, {
      method: "POST",
      body: form,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(typeof err.detail === "string" ? err.detail : JSON.stringify(err.detail));
    }
    return res.json();
  },

  async analyzeFsd(): Promise<AnalyzeResponse> {
    return fetchApi<AnalyzeResponse>("/analyze-fsd");
  },

  async generateTests(): Promise<GenerateResponse> {
    return fetchApi<GenerateResponse>("/generate-tests", { method: "POST" });
  },

  async regenerateTests(): Promise<RegenerateResponse> {
    return fetchApi<RegenerateResponse>("/regenerate-tests", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ confirm: true }),
    });
  },

  getReportUrl(filename: string): string {
    return `${API_BASE}/reports/${encodeURIComponent(filename)}`;
  },

  async fetchReportText(filename: string): Promise<string> {
    const res = await fetch(this.getReportUrl(filename));
    if (!res.ok) throw new Error("Rapport non trouvé");
    return res.text();
  },

  async listTests(): Promise<TestCase[]> {
    return fetchApi<TestCase[]>("/tests");
  },
};
