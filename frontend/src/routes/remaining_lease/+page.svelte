<script lang="ts">
	import { res, minMaxDates } from './data';
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import * as Plot from '@observablehq/plot';

	let year = minMaxDates.maxYear;
	let width: number;
	// let load = async function () {
	// 	const pq = await fetch(`/api/kv/hdb`);

	// 	const p = await db.registerFileBuffer('kv_pq', new Uint8Array(await pq.arrayBuffer()));
	// 	await db.registerFileURL('kv_pq_url', '/api/kv/hdb', DuckDBDataProtocol.HTTP, false);
	// 	// const res = await c.query(`
	// 	// SELECT COUNT(*) FROM read_parquet(kv_pq);
	// 	// `);
	// 	const res = await conn.query(`SELECT COUNT(*) FROM read_parquet(kv_pq_url)`);
	// 	return res;
	// };

	$: plotOpt = {
		width: width,
		marginTop: 30,
		marginLeft: 50,
		grid: true,
		color: { legend: true },
		marks: [
			Plot.dot(
				//{ length: res.numRows },
				res.toArray(),
				{
					x: 'lease_passed_year',
					y: 'avg_price',
					// fy: res.getChild('year_of_transaction'),
					// fx: res.getChild('flat_type'),
					opacity: 0.5,
					stroke: 'flat_type',
					tip: true,
					filter: (x) => x.year_of_transaction === year
				}
			),
			Plot.frame()
		]
	};
</script>

<input bind:value={year} type="range" min={minMaxDates.minYear} max={minMaxDates.maxYear} />
<span>{year}</span>

<div bind:clientWidth={width}>
	<ObsPlot {plotOpt} />
</div>
