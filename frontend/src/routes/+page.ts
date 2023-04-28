import { initDB } from '$lib/duckdb';
import { DuckDBDataProtocol } from '@duckdb/duckdb-wasm';

// need render on client because WebWorker is clientside only
export const ssr = false;

export async function load({ fetch }) {
	const duckdb = await initDB();
	const pq_data = await fetch('/api/blob_data');
	const pq_data_blob = await pq_data.blob();
	console.log(pq_data_blob);
	const parquetFile = new File([pq_data_blob], 'pq_file');
	await duckdb.registerFileHandle(
		'resale.parquet',
		parquetFile,
		DuckDBDataProtocol.BROWSER_FILEREADER,
		true
	);

	const another_data = await fetch('/api/blob_data');
	const pq_data_array = new Uint8Array(await another_data.arrayBuffer());
	await duckdb.registerFileBuffer('pq_file_buffer.parquet', pq_data_array);

	const c = await duckdb.connect();
	await c.query(`
			CREATE TABLE IF NOT EXISTS duplicated AS
			SELECT * FROM 'pq_file_buffer.parquet' UNION ALL SELECT * FROM 'resale.parquet';
		`);
	const res = await c.query(`
            SELECT 
				month, 
				avg(CAST(resale_price AS INTEGER)) AS avg_cost 
			FROM duplicated
			WHERE town = 'YISHUN' 
			GROUP BY month
			;
        `);
	return { result: res };
}
