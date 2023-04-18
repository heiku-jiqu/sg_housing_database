<script lang="ts">
	import { initDB } from '$lib/duckdb';
	import { chart } from '$lib/echarts';
	import { detach_before_dev, onMount } from 'svelte/internal';
	import { DuckDBDataProtocol } from '@duckdb/duckdb-wasm';
	async function load_db() {
		const duckdb = await initDB();
		const pq_data = await fetch('/api/blob_data');
		const pq_data_blob = await pq_data.blob();
		console.log(pq_data_blob);
		const parquetFile = new File([pq_data_blob], 'pq_file');
		await duckdb.registerFileHandle(
			'resale.parquet',
			parquetFile,
			DuckDBDataProtocol.BROWSER_FILEREADER,
			true
		);

		const another_data = await fetch('/api/blob_data');
		const pq_data_array = new Uint8Array(await another_data.arrayBuffer());
		await duckdb.registerFileBuffer('pq_file_buffer.parquet', pq_data_array);

		const c = await duckdb.connect();
		await c.query(`
			CREATE TABLE IF NOT EXISTS duplicated AS
			SELECT * FROM 'pq_file_buffer.parquet' UNION ALL SELECT * FROM 'resale.parquet';
		`);
		const res = await c.query(`
            SELECT 
				month, 
				avg(CAST(resale_price AS INTEGER)) AS avg_cost 
			FROM duplicated
			WHERE town = 'YISHUN' 
			AND resale_price > 600000
			GROUP BY month
			;
        `);
		return res;
	}
	let result_promise = load_db();
	$: opt = {
		title: {
			text: 'ECharts Getting Started Example'
		},
		xAxis: {
			data: ['shirt', 'cardigan', 'chiffon', 'pants', 'heels', 'socks']
		},
		yAxis: {},
		series: [
			{
				name: 'sales',
				type: 'bar',
				data: [5, 20, 36, 10, 10, 20]
			}
		]
	};
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

{#await result_promise then table}
	{table}
	<div style:height="400px" style:width="400px" use:chart={opt} />
{/await}
