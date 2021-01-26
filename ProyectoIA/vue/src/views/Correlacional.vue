<template>
  <div v-if="complete">
    <p class="text-h4">Matriz de Correlaciones</p>
    <!--<HeatMap v-if="correlaciones" :matriz="correlaciones"/>-->
    <v-data-table v-if="correlaciones"
      dense
      hide-default-footer
      :headers="headers"
      :items="correlaciones"
      item-key="name"
      class="">
    </v-data-table>
    <v-divider class="my-2"></v-divider>
    <p class="text-h4">Mapa de Calor</p>
    <div id="card" 
      :style="sizeCard"
      v-if="heatMap">
    <vocabgrid v-bind:correlacional="heatMap" v-bind:headers="headers"></vocabgrid>
    </div>
  </div>
</template>

<script>
import vocabgrid from '@/components/vocab-grid.vue';
import { mapActions, mapMutations, mapState } from "vuex";

import * as d3 from "d3";

export default {
  name: 'Correlacional',
  data() {
    return {
      correlaciones : null,
      heatMap: null,
      headers: null,
      complete:  false,
    }
  },
  components: {
    vocabgrid
  },
  computed: {
    //...mapState(["headers"]),
    sizeCard: function(){
      const size = Math.sqrt(this.heatMap.length);
      return {"max-width": (size * 80 + size *4) + "px"};
    }
  },
  mounted() {
    const promise = new Promise((resolve, reject) => {
        eel.get_correlaciones()((response) => {
          this.correlaciones = response.matriz.reverse();
          this.headers = response.headers;
          this.heatMap = response.map;
          resolve({});
        });
      });
    promise.then(() => {this.complete = true});
  },
}
</script>
<style>
#card {
  margin: auto auto;
  padding: 1.5em 0;
  border-radius: 4px;
}
</style>