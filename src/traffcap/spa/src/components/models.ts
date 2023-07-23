export interface Request {
  id: string;
  type: string;
  attributes: {
    endpoint_code: string;
    method: string;
    headers: string;
    query_params: string;
    body: string;
    id: number;
  }
}
