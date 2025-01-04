import { useFetch } from '@vueuse/core';
// import type { IRequest, IJSONAPIResource } from '@/types';
import { Repository, url } from '@/repositories/repository';

// Interface for request

interface IRequest {
    id: number,
    body: string,
    endpoint_code: string,
    headers: string,
    method: string,
    query_params: string
}


interface IJSONAPIResource<T> {
    id?: string,
    type: string,
    lid?: string,
    links?: string | null,
    meta?: string | null,
    relationships?: string | null,
    attributes?: T
}

interface IJSONAPIListRoot<T> {
    data: IJSONAPIResource<T>[]
}

interface IJSONAPIResourceRoot<T> {
    data: IJSONAPIResource<T>
}

export class TrafficRepository extends Repository {
    public static getAllTraffic(): Promise<IRequest[]> {
        return new Promise(traffic => {
            // const { data } = useFetch<IJSONAPIListRoot<IRequest>>(`${url}/traffic`).get().json();
            const { data } = useFetch(`${url}/traffic`).get();

            traffic([{
                id: 1,
                body: "",
                endpoint_code: "",
                headers: "",
                method: "",
                query_params: ""
            }]);
        });
    }
}
