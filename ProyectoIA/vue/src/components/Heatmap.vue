<template>
<div class="example">
  <apexchart :options="chartOptions" :series="matriz"></apexchart>
</div>
</template>

<script>
export default {
  name: 'Heatmap',
  props: ["matriz"],
  data: function() {
    return {
      chartOptions: {
        chart: {
          height: 350,
          type: 'heatmap',
        },
        plotOptions: {
          heatmap: {
            useFillColorAsStroke: true,
            colorScale: {
              ranges: [
                {
                  from: -1,
                  to: -1,
                  name: 'extreme',
                  color: '#FF0000'
                },
                {
                  from: -0.9999,
                  to: -0.8,
                  name: 'extreme',
                  color: '#FF7C0D'
                },
                {
                  from: -0.8999,
                  to: -0.3,
                  name: 'extreme',
                  color: '#ffc53e'
                },
                {
                  from: -0.0001,
                  to: -0.2999,
                  name: 'extreme',
                  color: '#128FD9'
                },
                {
                  from: 0,
                  to: 0,
                  name: 'extreme',
                  color: '#00A100'
                },
                {
                  from: 0.0001,
                  to: 0.2999,
                  name: 'extreme',
                  color: '#128FD9'
                },
                {
                  from: 0.3,
                  to: 0.7999,
                  name: 'extreme',
                  color: '#FFB200'
                },        
                {
                  from: 0.8,
                  to: 0.9999,
                  name: 'extreme',
                  color: '#FF7C0D'
                },     
                {
                  from: 1,
                  to: 1,
                  name: 'extreme',
                  color: '#FF0000'
                },       
              ]
            }
          }
        },
      },
    }
  },
}
</script>