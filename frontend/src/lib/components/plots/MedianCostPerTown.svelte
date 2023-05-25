<script lang="ts">
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import { initDB } from '$lib/duckdb';
	import type { DataType, Type } from 'apache-arrow';
	import * as Plot from '@observablehq/plot';

	async function loadData() {
		const duckdb = await initDB();
		const c = await duckdb.connect();
		const median_cost_per_month_per_town = c.query(`
            SELECT 
				town,
				month, 
				percentile_cont(0.5) WITHIN GROUP (ORDER BY resale_price) AS median_cost,
				dense_rank() OVER (ORDER BY town) AS facet_key
			FROM resale_hdb
			GROUP BY town, month
			ORDER BY town, month
			;
	`);
		return median_cost_per_month_per_town;
	}
	const promise = loadData();
</script>

{#await promise}
	<p>loading...</p>
{:then median_cost_per_month_per_town}
	<ObsPlot
		plotOpt={{
			marks: [
				Plot.line(
					median_cost_per_month_per_town.toArray().map((x) => ({ ...x, month: new Date(x.month) })),
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
							median_cost_per_month_per_town
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
{:catch error}
	<p style="color:red">{error.message}</p>
{/await}
