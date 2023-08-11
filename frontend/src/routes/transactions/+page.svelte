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
		const prep_statement = await c.prepare(`
			SELECT * FROM resale_hdb
			ORDER BY month DESC
			LIMIT ?
			;
		`);
		const result = await prep_statement.send(100000);
		await result.open(); // need to open the reader to get schema!!!
		arrow_table = new Arrow.Table(result.schema);
		for await (const batch of result) {
			let batch_table = new Arrow.Table(batch);
			arrow_table = arrow_table.concat(batch_table);
		}
	}
	get_data();
</script>

<a href="/">back to root</a>
<div>{arrow_table.numRows} rows loaded</div>
<div>
	<input
		type="range"
		min="0"
		max={arrow_table.numRows}
		bind:value={num_rows_to_show}
		style:width="100%"
	/>
	<input type="number" bind:value={num_rows_to_show} />
</div>
<br />

{#if arrow_table.numRows > 0}
	<table>
		<tr>
			{#each arrow_slice.schema.names as name}
				<th>{name}</th>
			{/each}
		</tr>
		{#each { length: arrow_slice.numRows } as _, i}
			<tr>
				{#each arrow_slice.schema.names as name}
					<td>{arrow_slice.get(i)[name]}</td>
				{/each}
			</tr>
		{/each}
	</table>
{/if}

<br />
{#if $avg_hdb_resale_store}
	<table>
		<tr>
			{#each $avg_hdb_resale_store.schema.names as name}
				<th>{name}</th>
			{/each}
		</tr>
		{#each Array(10)
			.fill(1)
			.map((_, i) => i + 1) as i}
			<tr>
				<td>
					{$avg_hdb_resale_store.get(i).month}
				</td>
				<td>
					{$avg_hdb_resale_store.get(i).avg_cost}
				</td>
			</tr>
		{/each}
	</table>
{/if}
