<script lang="ts">
	import '../styles.css';
	import { goto } from '$app/navigation';
</script>

<h1 on:click={() => goto('/')}>Housing Prices Trend</h1>

<slot />

<style>
	h1 {
		margin-top: 0;
		font-size: 2.5rem;
	}
	h1:hover {
		cursor: default;
	}
	h1:before {
		content: '';
		position: absolute;
		left: 1.7rem;
		top: 3.7rem;
		width: 0rem;
		transition: width 75ms ease-in;
		border-bottom: 4px solid blue;
		z-index: -1;
	}
	h1:hover:before {
		width: 22rem;
		transition: width 75ms ease-out;
	}
</style>
