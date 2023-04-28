<script lang="ts">
	import * as Plot from '@observablehq/plot';
	import { onMount } from 'svelte';

	export let chartData;
	export let plotOpt: Plot.PlotOptions = {
		marks: [Plot.line(chartData, { x: 'month', y: 'avg_cost' })],
		marginLeft: 70,
		style: {
			backgroundColor: 'transparent',
			width: '1200px'
		}
	};

	function plot(node: HTMLElement) {
		node.appendChild(Plot.plot(plotOpt));
	}
</script>

<div use:plot />
