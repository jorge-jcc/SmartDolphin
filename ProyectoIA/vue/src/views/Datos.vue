<template>
  <div>
  <div class="text-h4 my-5 ml-2">Data Set</div>
  <v-data-table v-if="table !== null"
    dense
    :headers="headers"
    :items="table"
    item-key="name"
    class=""
  ></v-data-table>
  </div>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";

export default {
  name: 'Datos',

  data: () => ({
  }),
  computed: {
    ...mapState(["headers", "table"]),
  },
  methods: {
    ...mapActions(["uploadFile", "getHeaders", "getTable"]),
    ...mapMutations(["reset"])
  },
  
}
</script>
