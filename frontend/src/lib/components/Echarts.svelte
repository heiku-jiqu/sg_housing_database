<script lang="ts">
	export let options;
	import { chart } from '$lib/echarts';
</script>

<div style:height="600px" style:width="1200px" use:chart={options} />
