<template>
  <v-container fluid>
    <v-overlay :value="loading" z-index="0" absolute>
      <v-progress-circular indeterminate color="purple" size="64"></v-progress-circular>
    </v-overlay>

    <v-tabs v-model="tab">
      <v-tab background-color="primary" v-for="item in items" :key="item.tab">
        {{ item.tab }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item v-for="item in items" :key="item.tab">
        <v-data-table v-if="item.table"
          dense
          :headers="headers"
          :items="item.table"
          item-key="name"
          class="">
        </v-data-table>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>

export default {
  name: 'Distancias',
  data() {
    return {
      loading : false,
      headers : null,
      table : null,
      tab: null,
      items: [
        { tab: 'Distancia Euclidiana', table: null },
        { tab: 'Distancia de Chebyshov', table: null },
        { tab: 'Distancia Manhattan', table: null },
        { tab: 'Distancia Minkowski', table: null },
      ],
    }
  },
  methods: {
    getDistancias(){
      this.loading = true;
      const promise = new Promise((resolve, reject) => {
        eel.get_distancias()((response) => {
          resolve(response);
        });
      });
      promise.then((response) => {
        this.headers = response.headers;
        this.items[0].table = response.euclidean;
        this.items[1].table = response.chebyshev;
        this.items[2].table = response.cityblock;
        this.items[3].table = response.minkowski;
        this.loading = false; 
      });
    }
  },
  mounted() {
    this.getDistancias()
  },
}
</script>
