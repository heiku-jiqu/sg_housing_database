import { initDB } from '$lib/duckdb';
import { DuckDBDataProtocol } from '@duckdb/duckdb-wasm';

// need render on client because WebWorker is clientside only
export const ssr = false;

export async function load({ fetch }) {
	const duckdb = await initDB();

	const [another_data, priv_resi_data] = await Promise.all([
		fetch('/api/blob_data/hdb'),
		fetch('/api/blob_data/private')
	]);

	const pq_data_array = new Uint8Array(await another_data.arrayBuffer());

	const pq_priv_resi_array = new Uint8Array(await priv_resi_data.arrayBuffer());

	await duckdb.registerFileBuffer('pq_file_buffer.parquet', pq_data_array);
	await duckdb.registerFileBuffer('pq_priv_resi.parquet', pq_priv_resi_array);

	const c = await duckdb.connect();
	await c.query(`
			CREATE TABLE IF NOT EXISTS resale_hdb AS
			SELECT * FROM 'pq_file_buffer.parquet';
		`);
	await c.query(`
			CREATE TABLE IF NOT EXISTS private_resi AS
			SELECT * FROM 'pq_priv_resi.parquet';
		`);

	console.log((await c.query(`SELECT * FROM private_resi LIMIT 10;`)).schema);
	console.log((await c.query(`SELECT * FROM resale_hdb LIMIT 10;`)).schema);
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
				percentile_cont(0.5) WITHIN GROUP (ORDER BY resale_price) AS median_cost,
				dense_rank() OVER (ORDER BY town) AS facet_key
			FROM resale_hdb
			GROUP BY town, month
			ORDER BY town, month
			;
	`);

	const cost_per_month_per_storey_range = await c.query(`
            SELECT 
				storey_range,
				month, 
				percentile_cont(0.5) WITHIN GROUP (ORDER BY resale_price) AS median_cost,
				avg(resale_price) AS avg_cost,
				dense_rank() OVER (ORDER BY storey_range) AS facet_key
			FROM resale_hdb
			GROUP BY storey_range, month
			ORDER BY storey_range, month
			;
	`);

	const vol_per_month = await c.query(`
		SELECT
			month,
			COUNT(*) as volume
		FROM resale_hdb
		GROUP BY month
		ORDER BY month
	`);

	// use prepared statements
	// use CUBE sql function
	return {
		avg_cost_per_month: avg_cost_per_month,
		median_cost_per_month_per_town: median_cost_per_month_per_town,
		cost_per_month_per_storey_range: cost_per_month_per_storey_range,
		vol_per_month: vol_per_month
	};
}
