<script>
	import { someData } from './data';
</script>

{#await someData() then data}
	{data}
{/await}
