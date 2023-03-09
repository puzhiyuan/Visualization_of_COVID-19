var ec_right2 = echarts.init(document.getElementById('r2'));


var ec_right2_option = {
    title : {
	    text : "全球确诊TOP10",
	    textStyle : {
	        color : 'white',
	    },
	    left : 'left'
	},
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#999'
        }
      }
    },
    toolbox: {
      feature: {
        dataView: { show: true, readOnly: false },
        magicType: { show: true, type: ['line', 'bar'] },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    legend: {
      data: ['确诊', '死亡']
    },
    xAxis: [
      {
        type: 'category',
        data: [],
        
        axisPointer: {
          type: 'shadow',
        },
        axisLabel: {
          fontSize: 7,
        }
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: '确诊',
        axisLabel: {
          show: true,
          color: 'white',
          fontSize: 12,
          formatter: function(value) {
            if (value >= 10000000) {
              value = value / 10000000 + 'kw';
            }
            return value;
			}
		},
      },
      {
        type: 'value',
        name: '死亡',
        axisLabel: {
			show: true,
			color: 'white',
			fontSize: 12,
			formatter: function(value) {
				if (value >= 1000) {
					value = value / 1000 + 'k';
				}
				return value;
			}
		},
      }
    ],
    series: [
      {
        name: '确诊',
        type: 'bar',
        data: []
      },
      {
        name: '死亡',
        type: 'line',
        yAxisIndex: 1,
        data: []
      }
    ]
};

ec_right2.setOption(ec_right2_option);
