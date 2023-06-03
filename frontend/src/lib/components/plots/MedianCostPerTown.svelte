<script lang="ts">
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import * as Plot from '@observablehq/plot';
	import { median_cost_per_month_per_town } from './store.ts';

	if (!$median_cost_per_month_per_town) {
		median_cost_per_month_per_town.init();
	}
</script>

{#if !$median_cost_per_month_per_town}
	<p>loading...</p>
{:else}
	<ObsPlot
		plotOpt={{
			marks: [
				Plot.line(
					$median_cost_per_month_per_town
						.toArray()
						.map((x) => ({ ...x, month: new Date(x.month) })),
					{
						x: 'month',
						y: 'median_cost',
						stroke: 'town',
						strokeOpacity: 0.5,
						tip: true,
						fy: (d) => Math.floor((Number(d.facet_key) - 1) / 3),
						fx: (d) => (Number(d.facet_key) - 1) % 3
					}
				),
				Plot.text(
					[
						...new Map(
							$median_cost_per_month_per_town
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
{/if}
