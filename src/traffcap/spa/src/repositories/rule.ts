import type { IRule, IJSONAPIListRoot, IJSONAPIResource } from '@/types';
import { Repository, url } from '@/repositories/repository';


export class RuleRepository extends Repository {
    public static async getAllRules(): Promise<IJSONAPIResource<IRule>[]> {
        return new Promise<IJSONAPIResource<IRule>[]>(async (rule) => {
            const response = await fetch(`${url}/rule`);
            if (!response.ok) {
                console.log("Error");
                return
            }
            const result: IJSONAPIListRoot<IRule> = (await response.json());
            rule(result.data);
        });
    }
}
