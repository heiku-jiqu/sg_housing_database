import { avg_hdb_resale_store } from '$lib/components/plots/store';
import { conn, tablesInitiated } from '$lib/duckdb2';
import * as Arrow from 'apache-arrow';
import { writable } from 'svelte/store';

await tablesInitiated;
await avg_hdb_resale_store.init();
const prep_statement = await conn.prepare(`
			SELECT * FROM resale_hdb
			ORDER BY month DESC
			LIMIT ?
			;
		`);
const result = await prep_statement.send(100000);
await result.open(); // need to open the reader to get schema!!!
export const tableStore = writable(new Arrow.Table(result.schema));
export const streamData = async () => {
	for await (const batch of result) {
		tableStore.update((table) => table.concat(new Arrow.Table(batch)));
	}
};
export { result as async_reader };