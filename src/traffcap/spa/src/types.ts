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
export interface IHeader {
  id: number,
  key: string,
  value: string
}

export interface IQueryParam {
  id: number,
  key: string,
  value: string
}

export interface IRequest {
  id: number,
  body: string,
  endpoint_code: string,
  headers: IHeader[],
  method: string,
  query_params: IQueryParam[],
  source_host: string,
  source_port: number,
  request_line: string,
  created_at: string
}

export interface IMatch {
  parent_id: number,
  rule_id: number,
  match_type: string,
  key?: string,
  pattern: string,
  invert: boolean,
  rule: IRule
}

export interface IRule {
  id: number,
  name: string,
  priority: number,
  content_type: string,
  template: string,
  matches: IMatch[],
  created_at: string
}
