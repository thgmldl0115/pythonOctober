$(document).ready(function () {
            var categories = {{ categories|tojson }};
            var series_data = {{ series_data|tojson }};

            // 기본 차트 렌더링
            var chart = Highcharts.chart('chart01', {
                title: { text: '수면 데이터' },
                subtitle: { text: 'sample : 241023 취침시' },
                yAxis: {
                    title: { text: '측정 무게 (g)' }
                },
                xAxis: {
                    categories: categories,
                    crosshair: true
                },
                series: series_data,
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle'
                }
            });

            // 버튼 클릭시 데이터 변경
            $('#changeData').click(function () {
                var newSeries = [{
                    name: '무게',
                    data: series_data[0].data.reverse()  // 데이터 역순 처리
                }];

                chart.update({
                    series: newSeries
                });
            });
        });