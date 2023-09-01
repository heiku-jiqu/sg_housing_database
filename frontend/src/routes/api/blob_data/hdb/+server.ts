import { supabase } from '$lib/supabase';
import type { RequestHandler } from '../$types';

export async function GET({ fetch, url }) {
	const { data, error } = await supabase.storage
		.from('sg-housing-db')
		//.download('resale.parquet.zstd');
		.download('merged_hdb_resale.parquet.zstd');
	if (error) {
		console.log('Error fetching hdb data');
		return new Response('Error fetching hdb data', {
			status: 500
		});
	} else {
		return new Response(data, {
			headers: {
				'Content-Type': 'application/octet-stream',
				'cache-control': 'public, max-age=14400'
			}
		});
	}
}
