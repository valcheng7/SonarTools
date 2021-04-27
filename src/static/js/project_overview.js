/**
 * ---------------------------------------
 * This demo was created using amCharts 4.
 *
 * For more information visit:
 * https://www.amcharts.com/
 *
 * Documentation is available at:
 * https://www.amcharts.com/docs/v4/
 * ---------------------------------------
 */

 let scatterBtn = document.querySelector("#click1");
 scatterBtn.addEventListener("click", function(){
    scatter()
  });

  let barBtn = document.querySelector("#click2");
  barBtn.addEventListener("click", function(){
     barChart()
   });


function scatter() {
    document.querySelector('.chart').innerHTML = '<div id="chartdiv" style="width: 100%;height:700px; background-color: #172b4d;"></div>';
    document.querySelector('#graph').style.height = "850px";
    document.querySelector('.chart').style.height = '';
    document.querySelector('#title').innerText = "No. of issues and duration of technical debt for each file"

    am4core.useTheme(am4themes_animated);
    am4core.useTheme(am4themes_dark);

    var chart = am4core.create("chartdiv", am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

    var valueAxisX = chart.xAxes.push(new am4charts.ValueAxis());
    var valueAxisY = chart.yAxes.push(new am4charts.ValueAxis());

    let topContainer = chart.chartContainer.createChild(am4core.Container);
    topContainer.layout = "absolute";
    topContainer.toBack();
    topContainer.paddingBottom = 15;
    topContainer.width = am4core.percent(100);

    let axisTitle = topContainer.createChild(am4core.Label);
    axisTitle.text = "y - Number Of Issues";
    axisTitle.fontWeight = 600;
    axisTitle.align = "left";
    axisTitle.paddingLeft = 10;

    var label = chart.chartContainer.createChild(am4core.Label);
    label.text = "x - Technical Debt";
    label.align = "center";
    label.paddingTop = 10;

    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.valueX = "x";
    series.dataFields.valueY = "y";
    series.dataFields.value = "value";
    series.strokeOpacity = 0;
    series.sequencedInterpolation = true;

    var bullet = series.bullets.push(new am4core.Circle());
    bullet.fill = am4core.color("#ffdd40");
    bullet.propertyFields.fill = "color";
    bullet.strokeOpacity = 0;
    bullet.radius = 7;
    bullet.strokeWidth = 2;
    bullet.fillOpacity = 0.7;
    bullet.stroke = am4core.color("#ffffff");

    bullet.tooltipText = "[bold]{title}:[/]\nTechnical Debt: {valueX.value} mins\nIssues: {valueY.value}";

    var hoverState = bullet.states.create("hover");
    hoverState.properties.fillOpacity = 1;
    hoverState.properties.strokeOpacity = 1;

    series.heatRules.push({ target: bullet, min: 2, max: 60, property: "radius" });

    bullet.adapter.add("tooltipY", function (tooltipY, target) {
        return -target.radius;
    })

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.behavior = "zoomXY";

    chart.scrollbarX = new am4core.Scrollbar();
    chart.scrollbarY = new am4core.Scrollbar();

    var scatterData = eval('('+document.querySelector('#scatter').innerText+')')

    let scatter = []
    for (const property in scatterData) {
        let dict = {};
        randomColour = '#' + Math.floor(Math.random()*16777215).toString(16).padStart(6, '0');
        dict.title = property;
        dict.color = randomColour;
        dict.x = scatterData[property][0];
        dict.y = scatterData[property][1];

        scatter.push(dict)
    }

    chart.data = scatter
}


scatter()

function barChart() {
    var barData = eval('('+document.querySelector('#bar').innerText+')')
    document.querySelector('.chart').innerHTML = '<canvas id="chart-sales-dark" class="chart-canvas"></canvas>';
    document.querySelector('#graph').style.height = "500px";
    document.querySelector('#title').innerText = "Comparison of severity levels"
    document.querySelector('.chart').style.height = ''
    var yaxis = ["Major", "Minor", "Critical", "Blocker", "Info"]
    var xaxis = [barData['MAJOR'], barData['MINOR'], barData['CRITICAL'], barData['BLOCKER'], barData['INFO']]
    var SalesChart = (function() {
        console.log(barData)
        // Variables
        var $chart = $('#chart-sales-dark');
        // Methods
        function init($chart) {
      
          var salesChart = new Chart($chart, {
            type: 'horizontalBar',
            options: {
              scales: {
                yAxes: [{
                  gridLines: {
                    lineWidth: 1,
                    color: Charts.colors.gray[900],
                    zeroLineColor: Charts.colors.gray[900]
                  },
                  legend: {
                      display: true
                      },
                  ticks: {
                    callback: function(value) {
                      if (!(value % 10)) {
                        return value;
                      }
                    }
                  }
                }]
              },
              tooltips: {
                callbacks: {
                  label: function(item, data) {
                    var label = data.datasets[item.datasetIndex].label || '';
                    var yLabel = item.xLabel;
                    var content = '';
      
                    if (data.datasets.length > 1) {
                      content += '<span class="popover-body-label mr-auto">' + label + '</span>';
                    }
      
                    content += yLabel;
                    return content;
                  }
                }
              }
            },
            data: {
              labels:  yaxis,
              datasets: [{
                label: 'Performance',
                data:  xaxis
              }]
            },
          });
      
          // Save to jQuery object
      
          $chart.data('chart', salesChart);
      
        };

        // Events
      
        if ($chart.length) {
          init($chart);
        }
      })();
}


