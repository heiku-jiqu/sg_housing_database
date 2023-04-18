import * as echarts from 'echarts';

const chart = function (node: HTMLElement, chartOpt: any) {
	var myChart = echarts.init(node);

	myChart.setOption({ ...chartOpt, height: 400, width: 400 });
};

export { chart };
