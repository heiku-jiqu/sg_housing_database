<script lang="ts">
	import Echarts from '$lib/components/Echarts.svelte';
	import ObsPlot from '$lib/components/ObsPlot.svelte';
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

<ObsPlot chartData={data.result.toArray().map((x) => ({ ...x, month: new Date(x.month) }))} />
