<script lang="ts">
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import { initDB } from '$lib/duckdb';
	import type { DataType, Type } from 'apache-arrow';
	import * as Plot from '@observablehq/plot';
	import { query_res } from './store';

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
			GROUP BY month
			ORDER BY month
			;
        `);
		query_res.set(avg_cost_per_month);
		return avg_cost_per_month;
	}
	const promise = loadData();
</script>

{#if $query_res}
	<ObsPlot
		plotOpt={{
			marks: [
				Plot.line(
					$query_res.toArray().map((x) => ({ ...x, month: new Date(x.month) })),
					{ x: 'month', y: 'avg_cost', tip: true }
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
{:else}
	<p>loading...</p>
{/if}
