<script lang="ts">
	import { avg_hdb_resale_store } from '$lib/components/plots/store';
	import { initDB } from '$lib/duckdb';
	import * as Arrow from 'apache-arrow';

	if (!$avg_hdb_resale_store) {
		avg_hdb_resale_store.init();
	}
	$: arrow_table = new Arrow.Table();

	let num_rows_to_show = 10;
	let arrow_slice: Arrow.Table;
	$: if (arrow_table.numRows > 0) {
		arrow_slice = arrow_table.slice(0, num_rows_to_show);
	}
	async function get_data() {
		const duckdb = await initDB();
		const c = await duckdb.connect();
		const result = await c.send<T>(`
			SELECT * FROM resale_hdb
			ORDER BY month DESC
			;
			`);
		await result.open(); // need to open the reader to get schema!!!
		arrow_table = new Arrow.Table(result.schema);
		for await (const batch of result) {
			let batch_table = new Arrow.Table(batch);
			console.log(batch_table.schema);
			arrow_table = arrow_table.concat(batch_table);
		}
	}
	get_data();
</script>

<a href="/">back to root</a>
<br />
{#if $avg_hdb_resale_store}
	{$avg_hdb_resale_store}
{/if}
