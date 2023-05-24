<script lang="ts">
	import Echarts from '$lib/components/Echarts.svelte';
	import ObsPlot from '$lib/components/ObsPlot.svelte';
	import AvgPrice from '$lib/components/plots/AvgPrice.svelte';
	import AvgPriceEcharts from '$lib/components/plots/AvgPriceEcharts.svelte';
	import TransactionVolume from '$lib/components/plots/TransactionVolume.svelte';
	import MedianCostPerTown from '$lib/components/plots/MedianCostPerTown.svelte';
	import * as Plot from '@observablehq/plot';
	export let data;
</script>

<AvgPriceEcharts />
<AvgPrice />
<TransactionVolume />
<MedianCostPerTown />
