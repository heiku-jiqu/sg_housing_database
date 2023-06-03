<script lang="ts">
	import { readable_query_res } from '$lib/components/plots/store';

	if (!$readable_query_res) {
		readable_query_res.init();
	}
</script>

<a href="/">back to root</a>
<br />
{#if $readable_query_res}
	{$readable_query_res}
{/if}
