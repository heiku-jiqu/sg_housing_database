<script lang="ts">
	import { priv_resi_store } from '$lib/stores';
	import { readable_query_res } from '$lib/components/plots/store';

	if (!$readable_query_res) {
		const promise = readable_query_res.init();
	}
</script>

<a href="/">back to root</a>
<br />
{#await $readable_query_res then}
	{$readable_query_res}
{/await}
