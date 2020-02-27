<script>
	import Graph from './Graph.svelte';
	import data from '../../data/sample.js';
</script>

<style>
	.chart {
		width: 100%;
		max-width: 1500px;
		height: calc(100% - 4em);
		min-height: 500px;
		max-height: 1000px;
		margin: 0 auto;
	}
</style>

<div class="chart">
	<Graph graph={data}/>
</div>