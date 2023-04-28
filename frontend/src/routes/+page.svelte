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

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

<Echarts options={opt} />
