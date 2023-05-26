import { writable } from 'svelte/store';
import { initDB } from '$lib/duckdb';

// use derived stores instead, which can do async set
export function createPrivDataStore() {
	const { subscribe, set } = writable();

	return {
		subscribe,
		init: async () => {
			const duckdb = await initDB();
			const c = await duckdb.connect();
			const avg_cost_per_month = await c.query(`
                SELECT 
                    month, 
                    avg(CAST(resale_price AS INTEGER)) AS avg_cost 
                FROM resale_hdb
                GROUP BY month
                ORDER BY month
                ;
            `);
			set(avg_cost_per_month);
		}
	};
}
export const priv_resi_store = createPrivDataStore();
