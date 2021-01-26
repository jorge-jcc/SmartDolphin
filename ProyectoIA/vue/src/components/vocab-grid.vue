<template>
  <div>
    <div v-for="(h, index) in head" v-bind:key="index" 
          :style="sqStyle"
          style="transform: rotate(-45deg)">
          <v-container fill-height fluid>
            <v-row align="center"
              justify="center">
              <v-col class="font-weight-light">
                {{h.text}}
              </v-col>
            </v-row>
          </v-container>
        </div>
    <div class="box" id="grid" :style="sizeBox">
          <div v-for="(n, index) in datos.length" 
            :style="sqStyle" id="grid" 
            :class="getColor(n)" 
            v-bind:key="index" class="text-center">
            <v-container fill-height fluid>
              <v-row align="center"
                justify="center">
                <v-col class="text-caption">
                  {{datos[n -1].value}}
                </v-col>
              </v-row>
            </v-container>
          </div>
        </div>
  </div>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";
  export default {
    name: 'vocabgrid',
    props:["correlacional", "headers"],
    data: function (){
    return {
      show: false,
      sqStyle: {
        width: '80px', 
        height: '80px', 
        margin: '2px', 
        display: 'inline-block', 
        borderRadius: '1.5px'
      },
      datos: this.correlacional,
      head: this.headers,
    }},
    computed: {
      sizeBox: function (){
        const size = Math.sqrt(this.datos.length);
        return {width: (size * 80 + size *4) + "px"};
      }
    },
    methods: {
      getColor(x) {
        var color, n = x-1;
        if (this.datos[n]){
          var stars = Math.abs(this.datos[n].value);
          color = stars == 1 ? 'blue-5'
          : stars >= 0.8 ? 'blue-4' 
          : stars >= 0.3 ? 'blue-3'
          : stars > 0 ? 'blue-2' 
          : 'gray-1';
          return color;
        } else return 'gray-1';
      }
    }
  }
</script>

<style>
.blue-1 { background-color: #84ffff; }
.blue-2 { background-color: #18ffff; }
.blue-3 { background-color: #00e5ff; }
.blue-4 { background-color: #00cee6; }
.blue-5 { background-color: #00b8d4; }
.gray-1 { background-color: #e7e7e7; }

.box { 
  margin: auto 0;
  padding: 0;
  line-height: 0;
  cursor: pointer;
}

#grid div:hover {
  transform: scale(1.15);
}
</style>