import { conn } from '$lib/duckdb2';

export const someData = async () => {
	const c = await conn;
	return await c.query(`SELECT * FROM (VALUES ('Amsterdam', 1), ('London', 2)) Cities(Name, Id);`);
};
