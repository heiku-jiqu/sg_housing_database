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
	$: monthYearLow = dateLow.toISOString().slice(0, 7);
	$: monthYearHigh = dateHigh.toISOString().slice(0, 7);
	function handleMove(event: InputEvent) {
		if (event.target?.name === 'low' && low > high) {
			high = low;
		} else if (event.target?.name === 'high' && high < low) {
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

<div class="range-slider">
	<span
		style="left:{((low - min) / (max - min)) * 100}%; right:{100 -
			((high - min) / (max - min)) * 100}%"
		class="range-selected"
	/>
</div>
<div class="range-input">
	<input on:input={handleMove} name="low" type="range" bind:value={low} {min} {max} {step} />
	<input on:input={handleMove} name="high" type="range" bind:value={high} {min} {max} {step} />
</div>

<br />
<div>
	<label for="low">low:</label>
	<input name="low" type="month" bind:value={monthYearLow} />
	<label for="high">high:</label>
	<input name="high" type="month" bind:value={monthYearHigh} />
</div>

<style>
	.range-slider {
		height: 5px;
		position: relative;
		background-color: #e1e9f6;
		border-radius: 2px;
	}
	.range-selected {
		height: 100%;
		left: 30%;
		right: 30%;
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
</style>
