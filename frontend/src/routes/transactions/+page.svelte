<script lang="ts">
	import DoubleRangeSlider from '$lib/components/DoubleRangeSlider.svelte';
	import { avg_hdb_resale_store } from '$lib/components/plots/store';
	import { tableStore as table, town, getData } from './data';

	let num_rows_to_show = 10;
	let selected: string = 'ANG MO KIO';
	let dateHigh: Date = new Date('12/1/2023');
	let dateLow: Date = new Date('1/1/2023');
	getData(selected, dateLow, dateHigh);

	const currency_formatter = new Intl.NumberFormat('en-US', {
		style: 'currency',
		currency: 'USD'
	});

	function prettyHeaders(s: string, sep: string = '_'): string {
		let x = s
			.split(sep)
			.map((x) => {
				let i = x.toLowerCase();
				return i[0].toUpperCase() + i.slice(1);
			})
			.join(' ');
		return x;
	}
</script>

<a href="/">back to root</a>
<div>{$table.numRows} rows loaded</div>

<div style:padding="10px">
	<DoubleRangeSlider
		bind:dateHigh
		bind:dateLow
		on:change={() => getData(selected, dateLow, dateHigh)}
	/>
</div>

<div class="dropdown">
	<select bind:value={selected} on:change={() => getData(selected, dateLow, dateHigh)}>
		{#each { length: town.numRows } as _, i}
			<option value={town.get(i)?.town}>{prettyHeaders(town.get(i)?.town, ' ')}</option>
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
				<th>{prettyHeaders(name.toString())}</th>
			{/each}
		</tr>
		{#each { length: num_rows_to_show } as _, i}
			<tr>
				{#each $table.schema.names as name}
					<td
						>{name === 'resale_price'
							? currency_formatter.format($table.get(i)?.[name])
							: $table.get(i)?.[name]}</td
					>
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
				<th>{prettyHeaders(name)}</th>
			{/each}
		</tr>
		{#each { length: $avg_hdb_resale_store.numRows } as _, i}
			<tr>
				<td>
					{new Date($avg_hdb_resale_store.get(i)?.month).toLocaleDateString('en-SG', {
						year: 'numeric',
						month: 'short'
					})}
				</td>
				<td>
					{currency_formatter.format($avg_hdb_resale_store.get(i)?.avg_cost)}
				</td>
			</tr>
		{/each}
	</table>
{/if}
