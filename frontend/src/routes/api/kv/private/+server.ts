import { supabase } from '$lib/supabase';
import type { RequestHandler } from '../$types';

export async function GET({ url }) {
	let data = await platform?.env.KV.get('priv_resi_parquet_zstd', {
		type: 'arrayBuffer',
		cacheTtl: 86400
	});
	return new Response(data, {
		headers: {
			'Content-Type': 'application/octet-stream'
		}
	});
}
