<script lang="ts">
	import * as Plot from '@observablehq/plot';
	import { fade } from 'svelte/transition';

	export let plotOpt: Plot.PlotOptions;

	function plot(node: HTMLElement) {
		node.appendChild(Plot.plot(plotOpt));
	}
</script>

<div use:plot in:fade />
