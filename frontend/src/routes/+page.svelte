<script lang="ts">
	import Echarts from '$lib/components/Echarts.svelte';
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import * as Plot from '@observablehq/plot';
	export let data;
</script>

<Echarts
	options={{
		dataset: {
			source: data.avg_cost_per_month.toArray()
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

<ObsPlot
	plotOpt={{
		marks: [
			Plot.line(
				data.avg_cost_per_month.toArray().map((x) => ({ ...x, month: new Date(x.month) })),
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

<ObsPlot
	plotOpt={{
		marks: [
			Plot.line(
				data.median_cost_per_month_per_town
					.toArray()
					.map((x) => ({ ...x, month: new Date(x.month) })),
				{
					x: 'month',
					y: 'median_cost',
					stroke: 'town',
					strokeOpacity: 0.5,
					fy: (d) => Math.floor((Number(d.facet_key) - 1) / 3),
					fx: (d) => (Number(d.facet_key) - 1) % 3
				}
			),
			Plot.text(
				[
					...new Map(
						data.median_cost_per_month_per_town
							.select(['town', 'facet_key'])
							.toArray()
							.map((x) => [x['town'], x])
					).values()
				],
				{
					text: (d) => d.town,
					fy: (d) => Math.floor((Number(d.facet_key) - 1) / 3),
					fx: (d) => (Number(d.facet_key) - 1) % 3,
					frameAnchor: 'top-left',
					dx: 6,
					dy: 6
				}
			),
			Plot.frame()
		],
		marginLeft: 70,
		style: {
			width: '1200px',
			backgroundColor: 'transparent'
		},
		grid: true,
		fx: { axis: null },
		fy: { axis: null }
	}}
/>
