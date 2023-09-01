import * as Arrow from 'apache-arrow';
import { avg_hdb_resale_store } from '$lib/components/plots/store';
/** @type {import('./$types').PageLoad} */
export async function load({ parent }) {
	const { streamed } = await parent();
	const c = await streamed?.dbconn;
	await streamed?.tablesInitiated;
	await avg_hdb_resale_store.init();
	const prep_statement = await c?.prepare(`
			SELECT * FROM resale_hdb
			ORDER BY month DESC
			LIMIT ?
			;
		`);
	const result = await prep_statement.send(100000);
	await result.open(); // need to open the reader to get schema!!!
	const arrow_table = new Arrow.Table(result.schema);

	return {
		arrow_table: arrow_table,
		async_reader: result
	};
}
