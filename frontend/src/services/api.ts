import { QueryRequest, QueryResponse } from '../types/api';

const API_BASE_URL = 'http://localhost:8000';

export const queryBook = async (request: QueryRequest): Promise<QueryResponse> => {
  const response = await fetch(`${API_BASE_URL}/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
};
