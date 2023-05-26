<script lang="ts">
	import { priv_resi_store } from '$lib/stores';
</script>

{#await priv_resi_store.init()}
	<p>awaiting promise...</p>
{:then}
	{$priv_resi_store.toArray()[0]}
{/await}
