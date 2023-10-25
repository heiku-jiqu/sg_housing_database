<script lang="ts">
	import * as Plot from '@observablehq/plot';
	import { fade } from 'svelte/transition';

	export let plotOpt: Plot.PlotOptions;

	function plot(node: HTMLElement, plotOpt: Plot.PlotOptions) {
		var plot = Plot.plot(plotOpt);
		node.appendChild(plot);
		return {
			update(plotOpt: Plot.PlotOptions) {
				node.replaceChildren(Plot.plot(plotOpt));
			}
		};
	}
</script>

<div use:plot={plotOpt} in:fade />
