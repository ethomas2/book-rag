export interface QueryRequest {
  query: string;
  chapter: number;
}

export interface QueryResponse {
  answer: string;
  quotes: string[];
}
