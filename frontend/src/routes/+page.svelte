<script lang="ts">
	import AvgPrice from '$lib/components/plots/AvgPrice.svelte';
	import AvgPriceEcharts from '$lib/components/plots/AvgPriceEcharts.svelte';
	import TransactionVolume from '$lib/components/plots/TransactionVolume.svelte';
	import MedianCostPerTown from '$lib/components/plots/MedianCostPerTown.svelte';

	const options = [
		{ chartName: 'AvgPriceEcharts', component: AvgPriceEcharts },
		{ chartName: 'AvgPrice', component: AvgPrice },
		{ chartName: 'TransactionVolume', component: TransactionVolume },
		{ chartName: 'MedianCostPerTown', component: MedianCostPerTown }
	];

	let selected = options[0];
</script>

{#each options as option}
	<button class="tabNav" on:click={() => (selected = option)} class:selected={selected === option}>
		{option.chartName}
	</button>
{/each}

<svelte:component this={selected.component} />

<style>
	.tabNav {
		font-size: 1.5rem;
		background-color: transparent;
		padding: 5px 20px;
		font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
		border-color: transparent;
	}
	.tabNav:hover {
		border: 2px solid;
		border-color: blue;
		transition: border-color 200ms ease-in;
	}

	.selected {
		color: blue;
		transition: color 200ms ease-in;
		font-weight: bold;
	}
</style>
