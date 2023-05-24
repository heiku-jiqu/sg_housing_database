<script lang="ts">
	import AvgPrice from '$lib/components/plots/AvgPrice.svelte';
	import AvgPriceEcharts from '$lib/components/plots/AvgPriceEcharts.svelte';
	import TransactionVolume from '$lib/components/plots/TransactionVolume.svelte';
	import MedianCostPerTown from '$lib/components/plots/MedianCostPerTown.svelte';
	export let data;
</script>

<AvgPriceEcharts />
<AvgPrice />
<TransactionVolume />
<MedianCostPerTown />
