<script>
	import '../styles.css';
</script>

<h1>Housing Prices Trend</h1>

<slot />

<style>
	h1 {
		margin-top: 0;
		font-size: 2.5rem;
	}
	h1:before {
		content: '';
		position: absolute;
		left: 1.7rem;
		top: 3.7rem;
		width: 3.2rem;
		transition: width 200ms ease-in-out;
		border-bottom: 4px solid blue;
		z-index: -1;
	}
	h1:hover:before {
		width: 22rem;
		transition: width 200ms ease-in-out;
	}
</style>
