<script lang="ts">
	import { initDB } from '$lib/duckdb';
	import '../styles.css';
	import {
		transaction_vol_store,
		median_cost_per_month_per_town,
		avg_hdb_resale_store,
		priv_residential_avg_cost
	} from '$lib/components/plots/store';
	import { goto } from '$app/navigation';
	import type { AsyncDuckDBConnection } from '@duckdb/duckdb-wasm';

	async function load_data() {
		// let x = await c.query(`SELECT * FROM private_resi_unnest LIMIT 10;`);
		// console.table(JSON.parse(JSON.stringify(x.toArray())));
	}
	const promise = load_data();

	// eagerly get query results

	// promise.then(() => {
	// 	transaction_vol_store.init();
	// 	median_cost_per_month_per_town.init();
	// 	avg_hdb_resale_store.init();
	// 	priv_residential_avg_cost.init();
	// });
</script>

<h1 on:click={() => goto('/')}>Housing Prices Trend</h1>

<slot />

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
