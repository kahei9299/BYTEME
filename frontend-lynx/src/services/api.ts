const API_BASE_URL = 'http://localhost:8080/api';

export interface AnalysisRequest {
  url: string;
  description?: string;
}

export interface AnalysisResponse {
  url: string;
  description: string;
  scores: {
    accuracy: number;
    homogeneity: number;
    comedy: number;
    theatrism: number;
    coherence: number;
  };
  averageScore: number;
  tier: string;
  advice: string;
}

export class ApiService {
  static async analyzeVideo(data: AnalysisRequest): Promise<AnalysisResponse> {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Analysis failed');
    }

    return response.json();
  }

  static async healthCheck(): Promise<{ status: string; message: string }> {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
  }
}