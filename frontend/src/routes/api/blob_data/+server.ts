import { supabase } from '$lib/supabase';
import type { RequestHandler } from './$types';

export async function GET({ url }) {
	const { data, error } = await supabase.storage
		.from('sg-housing-db')
		//.download('resale.parquet.zstd');
		.download('merged_hdb_resale.parquet.zstd');
	return new Response(data, { headers: { 'Content-Type': 'application/octet-stream' } });
}
