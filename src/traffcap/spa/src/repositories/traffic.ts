import type { IRequest, IJSONAPIListRoot, IJSONAPIResource } from '@/types';
import { Repository, url } from '@/repositories/repository';


export class TrafficRepository extends Repository {
    public static async getAllTraffic(): Promise<IJSONAPIResource<IRequest>[]> {
        return new Promise<IJSONAPIResource<IRequest>[]>(async (traffic) => {
            const response = await fetch(`${url}/traffic`);
            if (!response.ok) {
                console.log("Error");
                return
            }
            const result: IJSONAPIListRoot<IRequest> = (await response.json());
            traffic(result.data);
        });
    }
}
