<template>
  <v-container fluid>

    <v-dialog
      transition="dialog-top-transition"
      max-width="400"
      v-model="dialog">
      <v-card>
        <v-toolbar color="primary" dark>Error al seleccionar variables</v-toolbar>
          <v-card-actions class="justify-end">
            <v-btn
              text
              @click="dialog = false">
              Cerrar
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    <p class="text-h4">Selección de variables</p>
    <v-item-group multiple v-if="headers" class="mt-0 pt-0">
      <v-item v-for="(n, index) in headers"
        :key="index">
        <v-chip active-class="purple--text"
          :input-value="n.select"
          @click="updateHeaders(index)">
          {{ n.text }}
        </v-chip>
      </v-item>
    </v-item-group>
    <v-checkbox
      class="mt-0 mb-1"
      style="transform: scale(0.8); transform-origin:left"
      v-model="checkbox"
      label="Seleccionar todas"
      @click="select">
    </v-checkbox>
    <v-row justify="end" class="mr-5">
      <v-btn right color="primary"
        class="white--text"
        @click="updateDendogram">
          <v-icon
          left
          dark>
          mdi-cog
        </v-icon>
        Procesar
      </v-btn>
    </v-row>
    <v-divider class="my-2"></v-divider>
    <p class="text-h4">Dendrograma</p>
    <v-row>
      <v-col>
        <v-slider
          v-model="value"
          vertical
          @input="change"
          :min="min"
          :max="max">
        </v-slider>
      </v-col>
      <v-col cols="11" class="mx-2">
        <div id="container"></div>
      </v-col>
    </v-row>
    <v-divider class="my-2"></v-divider>
    <p class="text-h4">Análisis de Clústers</p>
    <v-layout>
      <v-row justify="center">
        <v-col cols="3">
          <v-text-field v-model="$v.form.clusters.$model"
            :error-messages="clusterErrors"
            label="Seleccione el número de Clústers"
            class="py-0 my-0">
          </v-text-field>
        </v-col>
        <v-col cols="1">
          <v-btn right color="primary"
            :disabled="$v.form.$invalid"
            class="white--text my-0"
            @click="updateClusters">
            <v-icon left dark>mdi-cog</v-icon>
            Procesar
          </v-btn>
        </v-col>
      </v-row>
    </v-layout>
    <v-layout>
      <v-row justify="center">
        <ClustersBar :series="seriesBar"/>
        <Clusters :series="seriesClusters"/>
      </v-row>
    </v-layout>
    <p class="text-h5">Medias de cada clúster</p>
    <v-data-table v-if="table !== null"
      dense
      :headers="headersTable"
      :items="table"
      item-key="name">
    </v-data-table>
  </v-container>
</template>
<script>
// @ is an alias to /src
import Clusters from '@/components/Clusters.vue';
import ClustersBar from '@/components/ClustersBar.vue';
import { required, numeric } from 'vuelidate/lib/validators';
import { validationMixin } from 'vuelidate';

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
  components: { Clusters, ClustersBar },
  name: 'ClusteringJerarquico',
  data() {
    return {
      dialog: false,
      headersTable: null,
      table: null,
      imagen: null,
      headers: null,
      checkbox: true,
      value: window.dMin,
      min: 0,
      max: 0,
      form:{
        clusters: 4,
      },
      seriesClusters: null,
      seriesBar: null,
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
          categories: [ 
          ],
          labels: {
            style: {
              colors: colors,
              fontSize: '12px'
            }
          }
        }
      }
    }
  },
  validations: {
    form:{
      clusters: { required, numeric },
    },
  },
  methods: {
    updateClusters(){
      let count = 0;
      this.headers.forEach((e) =>{
        if(e.select) count++;
      });
      if (count < 2) this.dialog = true;
      else{
        const promise = new Promise((resolve, reject) => {
          eel.get_clusters_jerarquico(this.headers, 
            this.$v.form.clusters.$model
          )((response) => {
            resolve(response);
          });
        });
        promise.then((response) => {
          this.seriesBar = response.count;
          //this.chartOptions.xaxis.categories = [];
          //for(let i = 0; i < response.count.length; i++)
            //this.chartOptions.xaxis.categories.push(i);
          this.headersTable = response.headers;
          this.table = response.table;
          this.seriesClusters = response.series;
          });
      }
    },
    updateHeaders(index){
      this.headers[index].select = ! this.headers[index].select;
      if (!this.headers[index].select)
        this.checkbox = false;
      else{
        let isAll = true;
        this.headers.forEach((e) =>{
          isAll = isAll && e.select;
        });
        this.checkbox = isAll;
      }
    },
    select(){
      this.headers.map((e) => { e.select = this.checkbox; });
    },
    change(){ 
      if (document.getElementById("container"))
        onThresholdChanged(this.value); 
    },
    updateDendogram(){
      let count = 0;
      this.headers.forEach((e) =>{
        if(e.select) count++;
      });
      if (count < 2) this.dialog = true;
      else{
        const promise = new Promise((resolve, reject) => {
          eel.get_jerarquico(this.headers)((response) => {
            resolve(response);
          });
        });
        promise.then((response) => {
          window.readData(response.dendrograma);
          this.min = window.dMin;
          this.max = window.dMax;  
        });
        if(!this.$v.form.$invalid)
          this.updateClusters();
      }
    }
  },
  computed: {
    clusterErrors(){
      const errors = []
      if (!this.$v.form.clusters.$dirty) return errors
      !this.$v.form.clusters.numeric && errors.push('Formato incorrecto')
      !this.$v.form.clusters.required && errors.push('Se requiere algún valor')
      return errors
    },
  },
  async mounted(){
    new Promise((resolve, reject) => {
        eel.get_headers_numeric()((response) => {
          resolve(response);
        });
      }).then((response) => {
        this.headers = Array();
        response.forEach(element => {
          this.headers.push({"text" : element.text, "select" : true});
        });
        this.updateClusters()
      });
    const promise = new Promise((resolve, reject) => {
      eel.get_jerarquico({})((response) => {
        resolve(response);
      });
    });
    window.initUI(); // Dendograma
    promise.then((response) => {
      window.readData(response.dendrograma); 
      this.min = window.dMin;
      this.max = window.dMax;
    });
  },
}
</script>
