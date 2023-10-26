import { conn, tablesInitiated } from '$lib/duckdb2';
import * as Arrow from 'apache-arrow';
import { writable } from 'svelte/store';

await tablesInitiated;

const c = await conn;
async function remaining_lease() {
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
		GROUP BY town, flat_type, year_of_transaction, lease_passed_year
		ORDER BY town, flat_type, year_of_transaction, lease_passed_year
		`);
	return res;
}

export const res = await remaining_lease();
export const minMaxDates = (
	await c.query(
		`
SELECT 
	MIN(CAST((month[:4]) AS INTEGER)) AS minYear,
	MAX(CAST((month[:4]) AS INTEGER)) AS maxYear,
FROM resale_hdb;`
	)
)
	.toArray()
	.flatMap((x) => x.toJSON())[0];
