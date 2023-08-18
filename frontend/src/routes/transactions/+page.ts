import * as Arrow from 'apache-arrow';
/** @type {import('./$types').PageLoad} */
export async function load({ parent }) {
	const { dbconn } = await parent();
	const c = dbconn;
	//avg_hdb_resale_store.init();
	const prep_statement = await c.prepare(`
			SELECT * FROM resale_hdb
			ORDER BY month DESC
			LIMIT ?
			;
		`);
	const result = await prep_statement.send(1000);
	await result.open(); // need to open the reader to get schema!!!
	let arrow_table = new Arrow.Table(result.schema);
	for await (const batch of result) {
		const batch_table = new Arrow.Table(batch);
		arrow_table = arrow_table.concat(batch_table);
	}
	return {
		arrow_table: arrow_table
	};
}
