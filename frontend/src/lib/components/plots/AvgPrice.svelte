<script lang="ts">
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import * as Plot from '@observablehq/plot';
	import { readable_query_res } from './store';

	if (!$readable_query_res) {
		readable_query_res.init();
	}
</script>

{#if $readable_query_res}
	<ObsPlot
		plotOpt={{
			marks: [
				Plot.line(
					$readable_query_res.toArray().map((x) => ({ ...x, month: new Date(x.month) })),
					{ x: 'month', y: 'avg_cost', tip: true }
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
{:else}
	<p>loading...</p>
{/if}
