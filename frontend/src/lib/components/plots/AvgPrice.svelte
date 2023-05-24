<script lang="ts">
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import { initDB } from '$lib/duckdb';
	import type { DataType, Type } from 'apache-arrow';
	import * as Plot from '@observablehq/plot';

	async function loadData() {
		const duckdb = await initDB();
		const c = await duckdb.connect();
		const avg_cost_per_month = await c.query<{
			month: DataType<Type.Utf8>;
			avg_cost: DataType<Type.Float32>;
		}>(`
            SELECT 
				month, 
				avg(CAST(resale_price AS INTEGER)) AS avg_cost 
			FROM resale_hdb
			WHERE town = 'YISHUN' 
			GROUP BY month
			ORDER BY month
			;
        `);
		return avg_cost_per_month;
	}
	const promise = loadData();
</script>

{#await promise}
	<p>loading...</p>
{:then avg_cost_per_month}
	<ObsPlot
		plotOpt={{
			marks: [
				Plot.line(
					avg_cost_per_month.toArray().map((x) => ({ ...x, month: new Date(x.month) })),
					{ x: 'month', y: 'avg_cost' }
				)
			],
			marginLeft: 70,
			style: {
				backgroundColor: 'transparent',
				width: '1200px'
			},
			grid: true
		}}
	/>
{:catch error}
	<p style="color:red">{error.message}</p>
{/await}
