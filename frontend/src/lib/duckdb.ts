import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import duckdb_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
// import duckdb_wasm_eh from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
// import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';

import type { AsyncDuckDB } from '@duckdb/duckdb-wasm';

let db: AsyncDuckDB | null = null;

const initDB = async () => {
	if (db) {
		return db;
	}

	const logger = new duckdb.ConsoleLogger();
	const worker = new Worker(duckdb_worker);

	db = new duckdb.AsyncDuckDB(logger, worker);
	await db.instantiate(duckdb_wasm, duckdb_worker);
	return db;
};
const connDB = async () => {
	db = await initDB();
	const c = await db.connect();
	return c;
};

export { initDB, connDB };
