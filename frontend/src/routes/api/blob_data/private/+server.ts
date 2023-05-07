import { supabase } from '$lib/supabase';
import type { RequestHandler } from '../$types';

export async function GET({ url }) {
	const { data, error } = await supabase.storage
		.from('sg-housing-db')
		.download('priv_residential.parquet.zstd');
	if (error) {
		console.log('Error fetching private residential data');
		return new Response('Error fetching private residential data', {
			status: 500
		});
	} else {
		return new Response(data, { headers: { 'Content-Type': 'application/octet-stream' } });
	}
}