<script lang="ts">
	import Echarts from '$lib/components/Echarts.svelte';
	import { readable_query_res } from './store';

	if (!$readable_query_res) {
		readable_query_res.init();
	}
</script>

{#if $readable_query_res}
	<Echarts
		options={{
			dataset: {
				source: $readable_query_res.toArray()
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
