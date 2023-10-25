<script lang="ts">
	export let dateLow: Date;
	export let dateHigh: Date;
	export let minDate = new Date('1/1/1990');
	export let maxDate = new Date('1/1/2024');
	let min = minDate.getTime();
	let max = maxDate.getTime();
	let low = dateLow.getTime();
	let high = dateHigh.getTime();
	let step = 24 * 60 * 60 * 1000;
	$: monthYearLow = dateLow.toLocaleDateString('en-CA', {
		year: 'numeric',
		month: '2-digit'
	});
	$: monthYearHigh = dateHigh.toLocaleDateString('en-CA', {
		year: 'numeric',
		month: '2-digit'
	});
	function handleMove(event: Event & { currentTarget: HTMLInputElement }) {
		if (event.currentTarget.name === 'low' && low > high) {
			high = low;
		} else if (event.currentTarget.name === 'high' && high < low) {
			low = high;
		}
		dateLow = new Date(low);
		dateHigh = new Date(high);
	}
	function formatDate(date: Date) {
		var monthNames = [
			'January',
			'February',
			'March',
			'April',
			'May',
			'June',
			'July',
			'August',
			'September',
			'October',
			'November',
			'December'
		];
		var monthIndex = date.getMonth();
		var year = date.getFullYear();

		return monthNames[monthIndex] + ' ' + year;
	}
</script>

<div class="slider-container">
	<div class="range-slider">
		<span
			style="left:{((low - min) / (max - min)) * 100}%; right:{100 -
				((high - min) / (max - min)) * 100}%"
			class="range-selected"
		/>
	</div>
	<div class="range-input">
		<input
			on:input={handleMove}
			on:change
			name="low"
			type="range"
			bind:value={low}
			{min}
			{max}
			{step}
		/>
		<input
			on:input={handleMove}
			on:change
			name="high"
			type="range"
			bind:value={high}
			{min}
			{max}
			{step}
		/>
	</div>
</div>

<div class="labels-container">
	<label for="low">{monthYearLow}</label>
	<label for="high">{monthYearHigh}</label>
</div>

<style>
	.range-slider {
		height: 5px;
		left: 2px;
		position: relative;
		background-color: #e1e9f6;
		border-radius: 2px;
	}
	.range-selected {
		height: 100%;
		position: absolute;
		border-radius: 5px;
		background-color: #1b53c0;
	}
	.range-input {
		position: relative;
	}
	input[type='range'] {
		width: 100%;
		top: -1em;
		position: absolute;
		background: none;
		pointer-events: none;
		appearance: none;
		-webkit-appearance: none;
		-moz-appearance: none;
		height: 20px;
	}
	input[type='range']::-webkit-slider-thumb {
		height: 20px;
		width: 20px;
		border-radius: 50%;
		border: 3px solid #1b53c0;
		background-color: #fff;
		pointer-events: auto;
		-webkit-appearance: none;
	}
	.labels-container {
		padding-top: 10px;
		width: 100%;
		display: inline-block;
	}
	.labels-container label:first-child {
		float: left;
		padding: 0.25em;
		border: 2px solid black;
	}
	.labels-container label:last-child {
		float: right;
		padding: 0.25em;
		border: 2px solid black;
	}
</style>
