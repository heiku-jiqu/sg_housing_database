import { initDB } from '$lib/duckdb.js';
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
		// initiate dl parquet duckdb
		// dl finish => load into tables => init stores
		// eagerly get query results
		const duckdb = initDB();
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

		const p = Promise.all([duckdb, pq_data_array, pq_priv_resi_array]).then(([db, d1, d2]) => {
			db?.registerFileBuffer('pq_file_buffer.parquet', d1);
			db?.registerFileBuffer('pq_priv_resi.parquet', d2);
		});
		const c = duckdb.then((db) => {
			return db?.connect();
		});
		const createdTablesPromise = Promise.all([c, p]).then(([c, p]) => {
			c?.query(`
				CREATE VIEW IF NOT EXISTS resale_hdb AS
				SELECT * FROM 'pq_file_buffer.parquet';
			`);
			c?.query(`
				CREATE VIEW IF NOT EXISTS private_resi AS
				SELECT * FROM 'pq_priv_resi.parquet';
			`);
			c?.query(`
				CREATE VIEW IF NOT EXISTS private_resi_unnest AS
				SELECT
					* EXCLUDE (transaction),
					UNNEST(transaction, recursive := TRUE)
				FROM private_resi;
			`);
		});
		const tablesInitiated = createdTablesPromise.then(() => {
			transaction_vol_store.init();
			median_cost_per_month_per_town.init();
			avg_hdb_resale_store.init();
			priv_residential_avg_cost.init();
		});

		return {
			streamed: {
				dbconn: c,
				tablesInitiated
			}
		};
	}
}
