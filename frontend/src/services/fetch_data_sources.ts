interface ApiResponse<T> {
  data: T;
  status: number;
}

class DataSourceService {
  private apiUrl: string;

  constructor() {
    this.apiUrl = import.meta.env.API_URL;
  }

  async get<T>(id: String): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.apiUrl}/data_sources`);
      const data = await response.json();
      return { data, status: response.status };
    } catch (error) {
      throw new Error(`API error: ${error.message}`);
    }
  }

  async post<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.apiUrl}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await response.json();
      return { data, status: response.status };
    } catch (error) {
      throw new Error(`API error: ${error.message}`);
    }
  }
}


export default new DataSourceService();