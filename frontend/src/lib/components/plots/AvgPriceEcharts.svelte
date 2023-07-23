<script lang="ts">
	import Echarts from '$lib/components/Echarts.svelte';
	import { avg_hdb_resale_store } from './store';

	if (!$avg_hdb_resale_store) {
		avg_hdb_resale_store.init();
	}
</script>

{#if $avg_hdb_resale_store}
	<Echarts
		options={{
			dataset: {
				source: $avg_hdb_resale_store.toArray()
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
