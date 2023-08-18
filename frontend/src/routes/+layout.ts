import { connDB, initDB, createTables } from '$lib/duckdb.js';
import {
	transaction_vol_store,
	median_cost_per_month_per_town,
	avg_hdb_resale_store,
	priv_residential_avg_cost
} from '$lib/components/plots/store';
import { browser } from '$app/environment';
export const prerender = true;
// need render on client because WebWorker is clientside only
export const ssr = false;

/** @type {import('./$types').LayoutServerLoad} */
export async function load({ data }) {
	if (browser) {
		const tables_loaded = createTables();
		// eagerly get query results
		tables_loaded.then(() => {
			transaction_vol_store.init();
			median_cost_per_month_per_town.init();
			avg_hdb_resale_store.init();
			priv_residential_avg_cost.init();
		});
		await tables_loaded;

		const c = await connDB();
		return {
			dbconn: c
		};
	}
}
