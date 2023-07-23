<script lang="ts">
	import { avg_hdb_resale_store } from '$lib/components/plots/store';

	if (!$avg_hdb_resale_store) {
		avg_hdb_resale_store.init();
	}
</script>

<a href="/">back to root</a>
<br />
{#if $avg_hdb_resale_store}
	{$avg_hdb_resale_store}
{/if}
