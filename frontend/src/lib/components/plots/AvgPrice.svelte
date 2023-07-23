<script lang="ts">
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import * as Plot from '@observablehq/plot';
	import { avg_hdb_resale_store } from './store';

	if (!$avg_hdb_resale_store) {
		avg_hdb_resale_store.init();
	}
</script>

{#if $avg_hdb_resale_store}
	<ObsPlot
		plotOpt={{
			marks: [
				Plot.line(
					$avg_hdb_resale_store.toArray().map((x) => ({ ...x, month: new Date(x.month) })),
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
