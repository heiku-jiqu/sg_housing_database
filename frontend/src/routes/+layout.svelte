<script>
	import { initDB } from '$lib/duckdb';
	import '../styles.css';
	import {
		transaction_vol_store,
		median_cost_per_month_per_town,
		avg_hdb_resale_store,
		priv_residential_avg_cost
	} from '$lib/components/plots/store';
	import { goto } from '$app/navigation';

	async function load_data() {
		const [duckdb, hdb_data, priv_resi_data] = await Promise.all([
			initDB(),
			fetch('/api/blob_data/hdb'),
			fetch('/api/blob_data/private')
		]);

		const [pq_data_array, pq_priv_resi_array] = await Promise.all([
			new Uint8Array(await hdb_data.arrayBuffer()),
			new Uint8Array(await priv_resi_data.arrayBuffer())
		]);

		await Promise.all([
			duckdb.registerFileBuffer('pq_file_buffer.parquet', pq_data_array),
			duckdb.registerFileBuffer('pq_priv_resi.parquet', pq_priv_resi_array)
		]);

		const c = await duckdb.connect();

		await Promise.all([
			c.query(`
			CREATE TABLE IF NOT EXISTS resale_hdb AS
			SELECT * FROM 'pq_file_buffer.parquet';
		`),
			c.query(`
			CREATE TABLE IF NOT EXISTS private_resi AS
			SELECT * FROM 'pq_priv_resi.parquet';
		`),
			c.query(`
			CREATE TABLE IF NOT EXISTS private_resi_unnest AS
			SELECT 
				* EXCLUDE (transaction), 
				UNNEST(transaction, recursive := TRUE)
			FROM private_resi;
		`)
		]);

		// let x = await c.query(`SELECT * FROM private_resi_unnest LIMIT 10;`);
		// console.table(JSON.parse(JSON.stringify(x.toArray())));
	}
	const promise = load_data();

	// eagerly get query results

	promise.then(() => {
		transaction_vol_store.init();
		median_cost_per_month_per_town.init();
		avg_hdb_resale_store.init();
		priv_residential_avg_cost.init();
	});
</script>

<h1 on:click={() => goto('/')}>Housing Prices Trend</h1>

{#await promise}
	<p>loading...</p>
{:then}
	<slot />
	<a href="/transactions">See transaction details</a>
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
		width: 0rem;
		transition: width 75ms ease-in;
		border-bottom: 4px solid blue;
		z-index: -1;
	}
	h1:hover:before {
		width: 22rem;
		transition: width 75ms ease-out;
	}
</style>
