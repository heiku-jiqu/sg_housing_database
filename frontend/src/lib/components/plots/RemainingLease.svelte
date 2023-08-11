<script>
	import { initDB } from '$lib/duckdb';
	import * as Arrow from 'apache-arrow';
	async function remaining_lease() {
		const duckdb = await initDB();
		const c = await duckdb.connect();
		const res = await c.query(`
		SELECT DISTINCT remaining_lease,
		CAST(regexp_extract(remaining_lease, '[0-9]+') AS INTEGER) AS remaining_lease_year 
		FROM resale_hdb ORDER BY remaining_lease;
		`);
		return res;
	}
</script>

{#await remaining_lease() then res}
	{#each res.toArray() as l}
		<table>
			<tr>
				<td>
					{l}
				</td>
			</tr>
		</table>
	{/each}
{/await}
