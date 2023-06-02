import { writable } from 'svelte/store';
import type * as arrow from 'apache-arrow';
// import type { Table } from '@duckdb/duckdb-wasm';

export const query_res = writable<
	arrow.Table<{
		month: arrow.DataType<arrow.Type.Utf8>;
		avg_cost: arrow.DataType<arrow.Type.Float32>;
	}>
>();
