<script lang="ts">
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import { initDB } from '$lib/duckdb';
	import type { DataType, Type } from 'apache-arrow';
	import * as Plot from '@observablehq/plot';

	async function loadData() {
		const duckdb = await initDB();
		const c = await duckdb.connect();
		const vol_per_month = c.query<{
			month: DataType<Type.Utf8>;
			volume: DataType<Type.Int32>;
		}>(`
		SELECT
			month,
			COUNT(*) as volume
		FROM resale_hdb
		GROUP BY month
		ORDER BY month
	`);
		return vol_per_month;
	}
	const promise = loadData();
</script>

{#await promise}
	<p>loading...</p>
{:then vol_per_month}
	<ObsPlot
		plotOpt={{
			marks: [
				Plot.rectY(
					vol_per_month.toArray().map((x) => ({ ...x, month: new Date(x.month) })),
					{
						x: 'month',
						y2: 'volume',
						fill: 'black',
						interval: 'month',
						insetLeft: 0.1,
						insetRight: 0.1,
						tip: true
					}
				)
			],
			marginLeft: 70,
			style: {
				width: '1200px',
				backgroundColor: 'transparent'
			}
		}}
	/>
{:catch error}
	<p style="color:red">{error.message}</p>
{/await}
