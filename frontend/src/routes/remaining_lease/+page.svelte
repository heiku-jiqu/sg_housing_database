<script>
	import RemainingLease from '$lib/components/plots/RemainingLease.svelte';
	import { initDB, connDB } from '$lib/duckdb';
	import { DuckDBDataProtocol } from '@duckdb/duckdb-wasm';
	let load = async function () {
		const c = await connDB();
		const db = await initDB();
		const pq = await fetch(`/api/kv/hdb`);

		const p = await db?.registerFileBuffer('kv_pq', new Uint8Array(await pq.arrayBuffer()));
		await db?.registerFileURL('kv_pq_url', '/api/kv/hdb', DuckDBDataProtocol.HTTP, false);
		// const res = await c.query(`
		// SELECT COUNT(*) FROM read_parquet(kv_pq);
		// `);
		const res = await c.query(`SELECT COUNT(*) FROM read_parquet(kv_pq_url)`);
		return res;
	};
	const res = load();
</script>

{#await res then r}
	{r}
{/await}
<RemainingLease />
