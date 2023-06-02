<script lang="ts">
	import Echarts from '$lib/components/Echarts.svelte';
	import { initDB } from '$lib/duckdb';
	import type { DataType, Type } from 'apache-arrow';
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
	<Echarts
		options={{
			dataset: {
				source: $query_res.toArray()
			},
			title: {
				text: 'ECharts Getting Started Example'
			},
			xAxis: { type: 'category' },
			yAxis: {},
			series: [
				{
					type: 'scatter',
					encode: {
						x: 'month',
						y: 'avg_cost'
					}
				}
			],
			tooltip: { show: true }
		}}
	/>
{:else}
	<p>loading...</p>
{/if}
