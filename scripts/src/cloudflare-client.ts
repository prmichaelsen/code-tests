import { config } from './config';

interface FetchOptions extends RequestInit {
  timeout?: number;
}

export class CloudflareClient {
  private baseURL = 'https://api.cloudflare.com/client/v4';
  private defaultTimeout = 30000;

  private getHeaders(): HeadersInit {
    return {
      'X-Auth-Email': config.email,
      'X-Auth-Key': config.apiKey,
      'Content-Type': 'application/json',
    };
  }

  private async fetchWithTimeout(
    url: string,
    options: FetchOptions = {}
  ): Promise<Response> {
    const { timeout = this.defaultTimeout, ...fetchOptions } = options;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        ...fetchOptions,
        signal: controller.signal,
        headers: {
          ...this.getHeaders(),
          ...fetchOptions.headers,
        },
      });
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error(`Request timeout after ${timeout}ms`);
      }
      throw error;
    }
  }

  private async request<T = any>(
    endpoint: string,
    options: FetchOptions = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    console.log(`[Request] ${options.method || 'GET'} ${endpoint}`);

    try {
      const response = await this.fetchWithTimeout(url, options);

      console.log(`[Response] ${response.status} ${endpoint}`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          `HTTP Error ${response.status}: ${JSON.stringify(errorData)}`
        );
      }

      // Handle empty responses
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        return {} as T;
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        console.error(`[Error] ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * Make a GET request to Cloudflare API
   */
  async get<T = any>(endpoint: string, options?: FetchOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  /**
   * Make a POST request to Cloudflare API
   */
  async post<T = any>(
    endpoint: string,
    data?: any,
    options?: FetchOptions
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * Make a PUT request to Cloudflare API
   */
  async put<T = any>(
    endpoint: string,
    data?: any,
    options?: FetchOptions
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * Make a PATCH request to Cloudflare API
   */
  async patch<T = any>(
    endpoint: string,
    data?: any,
    options?: FetchOptions
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * Make a DELETE request to Cloudflare API
   */
  async delete<T = any>(endpoint: string, options?: FetchOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' });
  }

  /**
   * Verify API credentials by fetching user details
   */
  async verifyCredentials(): Promise<boolean> {
    try {
      const response: any = await this.get('/user');
      console.log('✓ Credentials verified successfully');
      console.log(`  User: ${response.result.email}`);
      return true;
    } catch (error) {
      console.error('✗ Failed to verify credentials');
      return false;
    }
  }

  /**
   * List all zones (domains) in the account
   */
  async listZones(): Promise<any> {
    return this.get('/zones');
  }

  /**
   * Get zone details by zone ID
   */
  async getZone(zoneId: string): Promise<any> {
    return this.get(`/zones/${zoneId}`);
  }

  /**
   * List Cloudflare Pages projects
   */
  async listPagesProjects(): Promise<any> {
    if (!config.accountId) {
      throw new Error('CLOUDFLARE_ACCOUNT_ID is required for Pages operations');
    }
    return this.get(`/accounts/${config.accountId}/pages/projects`);
  }

  /**
   * Get details of a specific Pages project
   */
  async getPagesProject(projectName: string): Promise<any> {
    if (!config.accountId) {
      throw new Error('CLOUDFLARE_ACCOUNT_ID is required for Pages operations');
    }
    return this.get(`/accounts/${config.accountId}/pages/projects/${projectName}`);
  }

  /**
   * List deployments for a Pages project
   */
  async listPagesDeployments(projectName: string): Promise<any> {
    if (!config.accountId) {
      throw new Error('CLOUDFLARE_ACCOUNT_ID is required for Pages operations');
    }
    return this.get(
      `/accounts/${config.accountId}/pages/projects/${projectName}/deployments`
    );
  }

  /**
   * Create a new Pages deployment
   */
  async createPagesDeployment(projectName: string, data: any): Promise<any> {
    if (!config.accountId) {
      throw new Error('CLOUDFLARE_ACCOUNT_ID is required for Pages operations');
    }
    return this.post(
      `/accounts/${config.accountId}/pages/projects/${projectName}/deployments`,
      data
    );
  }

  /**
   * Get account details
   */
  async getAccount(): Promise<any> {
    if (!config.accountId) {
      throw new Error('CLOUDFLARE_ACCOUNT_ID is required');
    }
    return this.get(`/accounts/${config.accountId}`);
  }

  /**
   * List all accounts
   */
  async listAccounts(): Promise<any> {
    return this.get('/accounts');
  }
}

// Export singleton instance
export const cloudflare = new CloudflareClient();