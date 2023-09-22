<script lang="ts">
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import * as Plot from '@observablehq/plot';
	import { transaction_vol_store } from '$lib/components/plots/store';
</script>

{#if !$transaction_vol_store}
	<p>loading...</p>
{:else}
	<ObsPlot
		plotOpt={{
			marks: [
				Plot.rectY(
					$transaction_vol_store.toArray().map((x) => ({ ...x, month: new Date(x.month) })),
					{
						x: 'month',
						y: 'volume',
						fill: 'black',
						interval: 'month',
						insetLeft: 0.1,
						insetRight: 0.1
					}
				),
				Plot.tip(
					$transaction_vol_store.toArray().map((x) => ({ ...x, month: new Date(x.month) })),
					Plot.pointer({
						x: 'month',
						y: 'volume',
						anchor: 'bottom-left'
					})
				)
			],
			marginLeft: 70,
			style: {
				width: '1200px',
				backgroundColor: 'transparent'
			}
		}}
	/>
{/if}
