import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ScanRequest {
  url: string;
  max_pages?: number;
  include_external?: boolean;
}

export interface ScanResponse {
  scan_id: string;
  status: string;
  message: string;
}

