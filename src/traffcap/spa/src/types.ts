export interface IRequest {
    body: string,
    endpoint_code: string,
    headers: string,
    id: number,
    method: string,
    query_params: string
  };
  
export interface IJSONAPIResource<T> {
  id: string,
  lid?: string | null,
  links?: string | null,
  meta?: string | null,
  relationships?: string | null,
  type: string,
  attributes: T
};
