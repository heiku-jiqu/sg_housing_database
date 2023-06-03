import { writable } from 'svelte/store';
import type { Table, DataType, Type } from 'apache-arrow';
import { initDB } from '$lib/duckdb';

export function createQueryStore<
	T extends {
		[key: string]: DataType;
	} = any
>(query: string) {
	const { subscribe, set } = writable<Table<T>>();

	return {
		subscribe,
		init: async () => {
			const duckdb = await initDB();
			const c = await duckdb.connect();
			const result = await c.query<T>(query);
			set(result);
		}
	};
}

export const readable_query_res = createQueryStore<{
	month: DataType<Type.Utf8>;
	avg_cost: DataType<Type.Float32>;
}>(
	`
	SELECT 
    	month, 
    	avg(CAST(resale_price AS INTEGER)) AS avg_cost 
	FROM resale_hdb
	GROUP BY month
	ORDER BY month
	;`
);

export const transaction_vol_store = createQueryStore<{
	month: DataType<Type.Utf8>;
	volume: DataType<Type.Int32>;
}>(`
	SELECT
		month,
		COUNT(*) as volume
	FROM resale_hdb
	GROUP BY month
	ORDER BY month
`);

export const median_cost_per_month_per_town = createQueryStore<{
	town: DataType<Type.Utf8>;
	month: DataType<Type.Utf8>;
	median_cost: DataType<Type.Float32>;
	facet_key: DataType<Type.Int32>;
}>(`
	SELECT 
		town,
		month, 
		percentile_cont(0.5) WITHIN GROUP (ORDER BY resale_price) AS median_cost,
		dense_rank() OVER (ORDER BY town) AS facet_key
	FROM resale_hdb
	GROUP BY town, month
	ORDER BY town, month
	;
`);
