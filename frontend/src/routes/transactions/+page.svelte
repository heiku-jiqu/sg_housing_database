<script lang="ts">
	import { avg_hdb_resale_store } from '$lib/components/plots/store';
	import { tableStore as table, streamData, town, getData } from './data';

	let num_rows_to_show = 10;
	let selected: string;

	streamData();
</script>

<a href="/">back to root</a>
<div>{$table.numRows} rows loaded</div>
<div class="dropdown">
	<select bind:value={selected} on:change={() => getData(selected, 1000)}>
		{#each { length: town.numRows } as _, i}
			<option>{town.get(i)?.town}</option>
		{/each}
	</select>
</div>

<div>
	<input
		type="range"
		min="0"
		max={$table.numRows}
		bind:value={num_rows_to_show}
		style:width="100%"
	/>
	<input type="number" bind:value={num_rows_to_show} />
</div>
<br />

{#if $table.numRows > 0}
	<table>
		<tr>
			{#each $table.schema.names as name}
				<th>{name}</th>
			{/each}
		</tr>
		{#each { length: num_rows_to_show } as _, i}
			<tr>
				{#each $table.schema.names as name}
					<td>{$table.get(i)?.[name]}</td>
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
					{$avg_hdb_resale_store.get(i)?.month}
				</td>
				<td>
					{$avg_hdb_resale_store.get(i)?.avg_cost}
				</td>
			</tr>
		{/each}
	</table>
{/if}
