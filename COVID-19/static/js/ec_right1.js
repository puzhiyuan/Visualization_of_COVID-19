// var ec_right1 = echarts.init(document.getElementById('r1'));
// var ec_right1_option = {
// 	xAxis: {
// 	  data: ['Animals', 'Fruits', 'Cars']
// 	},
// 	yAxis: {},
// 	dataGroupId: '',
// 	animationDurationUpdate: 500,
// 	series: {
// 	  type: 'bar',
// 	  id: 'sales',
// 	  data: [
// 		{
// 		  value: 5,
// 		  groupId: 'animals'
// 		},
// 		{
// 		  value: 2,
// 		  groupId: 'fruits'
// 		},
// 		{
// 		  value: 4,
// 		  groupId: 'cars'
// 		}
// 	  ],
// 	  universalTransition: {
// 		enabled: true,
// 		divideShape: 'clone'
// 	  }
// 	}
//   };
//   const drilldownData = [
// 	{
// 	  dataGroupId: 'animals',
// 	  data: [
// 		['Cats', 4],
// 		['Dogs', 2],
// 		['Cows', 1],
// 		['Sheep', 2],
// 		['Pigs', 1]
// 	  ]
// 	},
// 	{
// 	  dataGroupId: 'fruits',
// 	  data: [
// 		['Apples', 4],
// 		['Oranges', 2]
// 	  ]
// 	},
// 	{
// 	  dataGroupId: 'cars',
// 	  data: [
// 		['Toyota', 4],
// 		['Opel', 2],
// 		['Volkswagen', 2]
// 	  ]
// 	}
//   ];
//   ec_right1.on('click', function (event) {
// 	if (event.data) {
// 	  var subData = drilldownData.find(function (data) {
// 		return data.dataGroupId === event.data.groupId;
// 	  });
// 	  if (!subData) {
// 		return;
// 	  }
// 	  ec_right1.setOption({
// 		xAxis: {
// 		  data: subData.data.map(function (item) {
// 			return item[0];
// 		  })
// 		},
// 		series: {
// 		  type: 'bar',
// 		  id: 'sales',
// 		  dataGroupId: subData.dataGroupId,
// 		  data: subData.data.map(function (item) {
// 			return item[1];
// 		  }),
// 		  universalTransition: {
// 			enabled: true,
// 			divideShape: 'clone'
// 		  }
// 		},
// 		graphic: [
// 		  {
// 			type: 'text',
// 			left: 50,
// 			top: 20,
// 			style: {
// 			  text: 'Back',
// 			  fontSize: 18
// 			},
// 			onclick: function () {
// 				ec_right1.setOption(ec_right1_option);
// 			}
// 		  }
// 		]
// 	  });
// 	}
//   });
// ec_right1.setOption(ec_right1_option)

var ec_right1 = echarts.init(document.getElementById('r1'));

var ec_right1_option   = {
	//标题样式
	title : {
	    text : "剩余确诊TOP5",
	    textStyle : {
	        color : 'white',
	    },
	    left : 'left'
	},
	color: ['#3398DB'],
	tooltip: {
		trigger: 'axis',
		axisPointer: {            // 坐标轴指示器，坐标轴触发有效
			type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
		}
	},
    xAxis: {
        type: 'category',
		 color : 'white',
        data: []
    },
    yAxis: {
        type: 'value',
		color : 'white',
		axisLine: {
			show: true
		},
		axisLabel: {
			show: true,
			color: 'white',
			fontSize: 12,
			formatter: function(value) {
				if (value >= 10000) {
					value = value / 10000 + 'w';
				}
				return value;
			}
		},
		//与x轴平行的线样式
		splitLine: {
			show: true,
			lineStyle: {
				// color: '#FFF',
				width: 1,
				// type: 'solid',
			}
		}
    },
    series: [{
        data: [],
        type: 'bar',
		// barMaxWidth:"50%"
    }]
};
ec_right1.setOption(ec_right1_option)



