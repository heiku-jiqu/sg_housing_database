import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import duckdb_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
// import duckdb_wasm_eh from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
// import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';

import type { AsyncDuckDB } from '@duckdb/duckdb-wasm';

let db: AsyncDuckDB | null = null;
let connection: duckdb.AsyncDuckDBConnection | null = null;
let connectionPromise: Promise<void> | null;

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
		return connection;
	}
	db = await initDB();
	connection = await db.connect();
	return connection;
};

export { initDB, connDB };
