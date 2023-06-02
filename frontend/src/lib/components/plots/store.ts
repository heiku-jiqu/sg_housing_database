import { writable } from 'svelte/store';
import type { Table, DataType, Type } from 'apache-arrow';
import { initDB } from '$lib/duckdb';
// import type { Table } from '@duckdb/duckdb-wasm';

export function createQueryStore() {
	const { subscribe, set } = writable();

	return {
		subscribe,
		init: async () => {
			console.log('init store');
			const duckdb = await initDB();
			const c = await duckdb.connect();
			const avg_cost_per_month = await c.query<{
				month: DataType<Type.Utf8>;
				avg_cost: DataType<Type.Float32>;
			}>(`
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
export const query_res = writable<
	Table<{
		month: DataType<Type.Utf8>;
		avg_cost: DataType<Type.Float32>;
	}>
>();

export const readable_query_res = createQueryStore();
