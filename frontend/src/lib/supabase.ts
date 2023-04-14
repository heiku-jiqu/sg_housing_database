import { createClient } from '@supabase/supabase-js';
import { env } from '$env/dynamic/private';

const supabase = createClient(env.SUPABASE_ENDPOINT, env.SUPABASE_SVC_KEY);

export { supabase };
