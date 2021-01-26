<template>
  <v-row justify="center">
    <div id="chart" v-if="series">
    <p class="text-h5 ml-5">Grupos de clústers</p>
      <apexchart type="scatter" 
        height="350" 
        width="600"
        :options="chartOptions" 
        :series="series">
      </apexchart>
    </div>
  </v-row>
</template>

<script>
  export default {
    name: 'Clusters',
    props:["series"],
    data: () => ({
      chartOptions: {
        chart: {
          height: 350,
          type: 'scatter',
          zoom: {
            enabled: true,
            type: 'xy'
          }
        },
        xaxis: {
          tickAmount: 10,
          labels: {
            formatter: function(val) {
              return parseFloat(val).toFixed(1)
            }
          }
        },
        yaxis: {
          tickAmount: 7
        }
      },
    })
  }
</script>
