import type { RequestHandler } from '../$types';
import { env } from '$env/dynamic/private';

export async function GET({ url, platform }) {
	let data = await platform?.env.KV.get('merged_hdb_resale_parquet_zstd', {
		type: 'arrayBuffer',
		cacheTtl: 86400
	});
	return new Response(data, {
		headers: {
			'Content-Type': 'application/octet-stream'
		}
	});
}
