/* JSONAPI Types */
export interface IJSONAPIResource<T> {
  id?: string,
  type: string,
  lid?: string,
  links?: string | null,
  meta?: string | null,
  relationships?: string | null,
  attributes?: T
}

export interface IJSONAPIListRoot<T> {
  data: IJSONAPIResource<T>[]
}

export interface IJSONAPIResourceRoot<T> {
  data: IJSONAPIResource<T>
}

/* All other types */
export interface IRequest {
  id: number,
  body: string,
  endpoint_code: string,
  headers: string,
  method: string,
  query_params: string,
  source_host: string,
  source_port: number,
  request_line: string,
  created_at: string
}
