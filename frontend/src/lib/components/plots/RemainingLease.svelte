<script lang="ts">
	import { conn, createdTablesPromise } from '$lib/duckdb2';
	import ObsPlot from '../ObsPlot.svelte';
	import * as Plot from '@observablehq/plot';
	$: town = 'JURONG EAST';
	async function remaining_lease() {
		await createdTablesPromise;
		const c = await conn;
		const res = await c.query(`
		WITH tbl AS (
			SELECT *, 
			CAST((month[:4]) AS INTEGER) AS year_of_transaction ,
			year_of_transaction - CAST(lease_commence_date AS INTEGER) AS lease_passed_year,
			CAST(regexp_extract(remaining_lease, '[0-9]+') AS INTEGER) AS remaining_lease_year,
			FROM resale_hdb ORDER BY remaining_lease_year
		)
		SELECT 
		town, flat_type, year_of_transaction, lease_passed_year,
			avg(resale_price) AS avg_price,
			median(resale_price) AS median_price,
		FROM tbl 
		-- WHERE town = '${town}'
		GROUP BY town, flat_type, year_of_transaction, lease_passed_year
		ORDER BY town, flat_type, year_of_transaction, lease_passed_year
		`);
		return res;
	}
	let year = 2000;
</script>

<input bind:value={year} type="range" min="1990" max="2023" />
<span>{year}</span>

{#await remaining_lease() then res}
	<ObsPlot
		plotOpt={{
			grid: true,
			marks: [
				Plot.dot(
					{ length: res.numRows },
					{
						x: res.getChild('lease_passed_year'),
						y: res.getChild('avg_price'),
						// fy: res.getChild('year_of_transaction'),
						// fx: res.getChild('flat_type'),
						opacity: 0.5,
						stroke: res.getChild('flat_type'),
						tip: true,
						filter: res
							.getChild('year_of_transaction')
							?.toArray()
							.map((x) => x === year)
					}
				),
				Plot.frame()
			]
		}}
	/>
{/await}
