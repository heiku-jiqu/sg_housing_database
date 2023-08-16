import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import duckdb_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
// import duckdb_wasm_eh from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
// import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';

import type { AsyncDuckDB } from '@duckdb/duckdb-wasm';

let db: AsyncDuckDB | null = null;
let connection: duckdb.AsyncDuckDBConnection | undefined = undefined;
let connectionPromise: Promise<void> | null;
let createdTablesPromise: Promise<any> | null;

const initDB = async () => {
	if (!connectionPromise) {
		const logger = new duckdb.ConsoleLogger();
		const worker = new Worker(duckdb_worker);

		db = new duckdb.AsyncDuckDB(logger, worker);
		connectionPromise = await db.instantiate(duckdb_wasm, duckdb_worker);
	}

	return db;
};
const connDB = async () => {
	if (connection) {
		return connection as duckdb.AsyncDuckDBConnection;
	}
	db = await initDB();
	connection = await db?.connect();
	return connection as duckdb.AsyncDuckDBConnection;
};
const createTables = async () => {
	const c = await connDB();
	if (!createdTablesPromise) {
		createdTablesPromise = Promise.all([
			c.query(`
			CREATE VIEW IF NOT EXISTS resale_hdb AS
			SELECT * FROM 'pq_file_buffer.parquet';
		`),
			c.query(`
			CREATE VIEW IF NOT EXISTS private_resi AS
			SELECT * FROM 'pq_priv_resi.parquet';
		`),
			c.query(`
				CREATE VIEW IF NOT EXISTS private_resi_unnest AS
				SELECT
					* EXCLUDE (transaction),
					UNNEST(transaction, recursive := TRUE)
				FROM private_resi;
			`)
		]);
	}
	return createdTablesPromise;
};

export { initDB, connDB, createTables };
