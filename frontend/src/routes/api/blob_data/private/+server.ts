import { supabase } from '$lib/supabase';
import type { RequestHandler } from '../$types';

export async function GET({ fetch, url }) {
	const pubUrl = await supabase.storage
		.from('sg-housing-db')
		.getPublicUrl('priv_residential.parquet.zstd');
	return fetch(pubUrl.data.publicUrl);
}
