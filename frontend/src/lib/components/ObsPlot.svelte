<script lang="ts">
	import * as Plot from '@observablehq/plot';
	import { onMount } from 'svelte';

	export let plotOpt: Plot.PlotOptions;

	function plot(node: HTMLElement) {
		node.appendChild(Plot.plot(plotOpt));
	}
</script>

<div use:plot />
