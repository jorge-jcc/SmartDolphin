<template>
  <v-row justify="center">
    <div id="chart" v-if="series">
      <p class="text-h5 ml-5">Cantidad de datos en cada clúster</p>
      <apexchart type="bar" 
        height="350" 
        width="600"
        :options="chartOptions" 
        :series="series">
      </apexchart>
    </div>
  </v-row>
</template>

<script>
  var colors = [
    '#008FFB',
    '#00E396',
    '#FEB019',
    '#FF4560',
    '#775DD0',
    '#546E7A',
    '#26a69a',
    '#D10CE8'
  ];
  export default {
    name: 'ClustersBar',
    props:["series"],
    data: () => ({
      chartOptions: {
        chart: {
          height: 350,
          type: 'bar',
        },
        colors: colors,
        plotOptions: {
          bar: {
            columnWidth: '45%',
            distributed: true
          }
        },
        dataLabels: {
          enabled: false
        },
        legend: {
          show: false
        },
        xaxis: {
          categories: []
        }
      }
    })
  }
</script>
