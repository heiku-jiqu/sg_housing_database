import { initDB } from '$lib/duckdb';
import { DuckDBDataProtocol } from '@duckdb/duckdb-wasm';

// need render on client because WebWorker is clientside only
export const ssr = false;

export async function load({ fetch }) {
	const duckdb = await initDB();
	// const pq_data = await fetch('/api/blob_data');
	// const pq_data_blob = await pq_data.blob();
	// console.log(pq_data_blob);
	// const parquetFile = new File([pq_data_blob], 'pq_file');
	// await duckdb.registerFileHandle(
	// 	'resale.parquet',
	// 	parquetFile,
	// 	DuckDBDataProtocol.BROWSER_FILEREADER,
	// 	true
	// );

	const another_data = await fetch('/api/blob_data');
	const pq_data_array = new Uint8Array(await another_data.arrayBuffer());
	await duckdb.registerFileBuffer('pq_file_buffer.parquet', pq_data_array);

	const c = await duckdb.connect();
	await c.query(`
			CREATE TABLE IF NOT EXISTS resale_hdb AS
			SELECT * FROM 'pq_file_buffer.parquet';
		`);
	const schema = await c.query(`SELECT * FROM resale_hdb LIMIT 10;`);
	console.log(schema);
	const avg_cost_per_month = await c.query(`
            SELECT 
				month, 
				avg(CAST(resale_price AS INTEGER)) AS avg_cost 
			FROM resale_hdb
			WHERE town = 'YISHUN' 
			GROUP BY month
			ORDER BY month
			;
        `);

	const median_cost_per_month_per_town = await c.query(`
            SELECT 
				town,
				month, 
				percentile_cont(0.5) WITHIN GROUP (ORDER BY resale_price) AS median_cost 
			FROM resale_hdb
			GROUP BY town, month
			ORDER BY town, month
			;
	`);

	const cost_per_month_per_storey_range = await c.query(`
            SELECT 
				town,
				month, 
				percentile_cont(0.5) WITHIN GROUP (ORDER BY resale_price) AS median_cost,
				avg(resale_price) AS avg_cost 
			FROM resale_hdb
			GROUP BY storey_range, month
			ORDER BY storey_range, month
			;
	`);
	return {
		avg_cost_per_month: avg_cost_per_month,
		median_cost_per_month_per_town: median_cost_per_month_per_town
	};
}
