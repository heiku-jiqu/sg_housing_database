import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import duckdb_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
// import duckdb_wasm_eh from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
// import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';

import {
	transaction_vol_store,
	median_cost_per_month_per_town,
	avg_hdb_resale_store,
	priv_residential_avg_cost
} from '$lib/components/plots/store';

const initDB = async () => {
	const logger = new duckdb.ConsoleLogger();
	const worker = new Worker(duckdb_worker);

	const db = new duckdb.AsyncDuckDB(logger, worker);
	await db.instantiate(duckdb_wasm, duckdb_worker);
	return db;
};

const downloadData = async () => {
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
	return Promise.all([pq_data_array, pq_priv_resi_array]);
};

const db_promise = initDB();
const dl_promise = downloadData();
const register_promise = Promise.all([db_promise, dl_promise]).then(([db, [d1, d2]]) => {
	db.registerFileBuffer('pq_file_buffer.parquet', d1);
	db.registerFileBuffer('pq_priv_resi.parquet', d2);
});

const db = await db_promise;
const conn = await db.connect();
const createdTablesPromise = Promise.all([register_promise, conn]).then(([r, c]) => {
	c.query(`
	CREATE VIEW IF NOT EXISTS resale_hdb AS
	SELECT * FROM 'pq_file_buffer.parquet';
`);
	c.query(`
	CREATE VIEW IF NOT EXISTS private_resi AS
	SELECT * FROM 'pq_priv_resi.parquet';
`);
	c.query(`
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

export { db, conn, createdTablesPromise, tablesInitiated };
