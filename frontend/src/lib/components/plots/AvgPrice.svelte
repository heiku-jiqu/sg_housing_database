<script lang="ts">
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import * as Plot from '@observablehq/plot';
	import { avg_hdb_resale_store } from './store';
</script>

{#if $avg_hdb_resale_store}
	<ObsPlot
		plotOpt={{
			x: { type: 'utc' },
			marks: [
				Plot.line(
					{ length: $avg_hdb_resale_store.numRows },
					{
						x: $avg_hdb_resale_store.getChild('month'),
						y: $avg_hdb_resale_store.getChild('avg_cost'),
						tip: true
					}
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
