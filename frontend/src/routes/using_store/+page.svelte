<script lang="ts">
	import { priv_resi_store } from '$lib/stores';
	import { readable_query_res } from '$lib/components/plots/store';

	async function hello() {
		console.log('initing');
		await readable_query_res.init();
	}

	hello();
</script>

{#if $readable_query_res}
	{$readable_query_res}
{:else}
	<p>dogshit</p>
{/if}
