<script lang="ts">
	import { res } from './data';
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import * as Plot from '@observablehq/plot';

	let year = 2020;
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
						.map((x: number) => x === year)
				}
			),
			Plot.frame()
		]
	};
</script>

<input bind:value={year} type="range" min="1990" max="2023" />
<span>{year}</span>

<div bind:clientWidth={width}>
	<ObsPlot {plotOpt} />
</div>
