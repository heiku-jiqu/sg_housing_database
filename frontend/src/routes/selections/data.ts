import { conn } from '$lib/duckdb2';

export const someData = async () => {
	return await conn.query(
		`SELECT * FROM (VALUES ('Amsterdam', 1), ('London', 2)) Cities(Name, Id);`
	);
};
