<script lang="ts">
	import Echarts from '$lib/Echarts.svelte';
	export let data;

	$: opt = {
		dataset: {
			source: data.result.toArray()
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
	};
</script>

<Echarts options={opt} />
