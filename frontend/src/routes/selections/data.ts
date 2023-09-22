import { conn } from '$lib/duckdb2';

export const someData = async () => {
	const pq_data_array = fetch('/api/blob_data/hdb')
		.then((x) => {
			return x.arrayBuffer();
		})
		.then((x) => {
			return new Uint8Array(x);
		});
	const pq_priv_resi_array = fetch('/api/blob_data/private')
		.then((x) => {
			return x.arrayBuffer();
		})
		.then((x) => {
			return new Uint8Array(x);
		});

	const p = Promise.all([pq_data_array, pq_priv_resi_array]);
	await p;
	return await conn.query(
		`SELECT * FROM (VALUES ('Amsterdam', 1), ('London', 2)) Cities(Name, Id);`
	);
};
