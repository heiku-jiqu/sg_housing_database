import * as echarts from 'echarts';

const chart = function (node: HTMLElement, chartOpt: any) {
	let myChart = echarts.init(node, null, { renderer: 'svg' });

	myChart.setOption({ ...chartOpt });
};

export { chart };
