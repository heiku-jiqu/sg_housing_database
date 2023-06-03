<script>
	// need render on client because WebWorker is clientside only
	export const ssr = false;
	import { initDB } from '$lib/duckdb';
	import '../styles.css';
	async function load_data() {
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
	}
	const promise = load_data();
</script>

<h1>Housing Prices Trend</h1>

{#await promise then}
	<slot />
	<a href="/using_store">go to</a>
{/await}

<style>
	h1 {
		margin-top: 0;
		font-size: 2.5rem;
	}
	h1:before {
		content: '';
		position: absolute;
		left: 1.7rem;
		top: 3.7rem;
		width: 3.2rem;
		transition: width 200ms ease-in-out;
		border-bottom: 4px solid blue;
		z-index: -1;
	}
	h1:hover:before {
		width: 22rem;
		transition: width 200ms ease-in-out;
	}
</style>
