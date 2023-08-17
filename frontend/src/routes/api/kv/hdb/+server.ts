import type { RequestHandler } from '../$types';
import { env } from '$env/dynamic/private';

export async function GET({ url, platform }) {
	let data = await platform?.env.KV.get('merged_hdb_resale_parquet_zstd');
	return new Response(data);
}
