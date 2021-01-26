<template>
  <v-app>
    <v-navigation-drawer app permanent color="deep-green accent-4" dark>
      <v-list-item class="px-2">
        <v-list-item-avatar>
          <v-img width="100" src="./assets/delfin.png"></v-img>
        </v-list-item-avatar>
        <v-list-item-title>Smart Dolphin</v-list-item-title>
      </v-list-item>
      <v-divider></v-divider>
      <v-list dense flat>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-list-item v-bind="attrs" v-on="on">
              <v-list-item-icon><v-icon>mdi-folder-outline</v-icon></v-list-item-icon>
              <v-list-item-content><v-list-item-title>Archivos</v-list-item-title></v-list-item-content>
            </v-list-item>
          </template>
          <v-card>
            <v-card-title class="justify-center">
              <span class="headline">Cargar Archivo</span>
            </v-card-title>
            <v-card-text >
              <v-container class="pt-0">
                <v-row>
                  <v-col cols="12" class="pt-0">
                    <v-file-input v-model="$v.file.$model"
                      accept=".csv,.json,.xlsx,.xls,.txt"
                      hide-details=""
                      placeholder="Archivo"
                      @change="updateFile">
                    </v-file-input>
                    <v-switch class="mt-0 mb-1"
                      style="transform: scale(0.8); transform-origin:left"
                      v-model="header"
                      hide-details=""
                      label="Incluir Cabeceras">
                    </v-switch>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field label="*Separadores"></v-text-field>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field  label="*Salto de línea"></v-text-field>
                  </v-col>
                </v-row>
                <small>*Solo si aplica</small>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="red darken-1" text @click="dialog = false">Cancelar</v-btn>
              <v-btn color="purple darken-2" :disabled="$v.file.$invalid" text @click="cargarArchivo">
                Cargar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-list-item
          v-for="(item, index) in itemAppBar" 
          :key="index"
          :to="item.route"
          :disabled="item.disabled"
          link>
          <v-list-item-icon><v-icon>{{ item.icon }}</v-icon></v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main class="grey lighten-5">
      <v-overlay :value="overlay">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";
import { required } from 'vuelidate/lib/validators'

export default {
  name: 'App',
  components: {
  },
  data: () => ({
    drawer: true,
    file: null,
    typeFile: null,
    header: true,
    overlay: false,
    columnas: null,
    settings: [],
    items: [
          { title: 'Home'},
          { title: 'About'},
        ],
        links: ['Home', 'Contacts', 'Settings'],
        mini: true,
    itemNavDrawer: ['mdi-folder-outline', 'mdi-file-tree'],
    itemAppBar: [
      {name: 'Datos', route: '/datos', icon: 'mdi-file-tree', disabled: true}, 
      {name: 'Reglas de Asociación', route: '/asociacion', icon: 'mdi-shape', disabled: true}, 
      {name: 'Analisis Correlacional', route: '/correlacional', icon: 'mdi-chart-scatter-plot-hexbin', disabled: true}, 
      {name: 'Distancias', route: '/distancias', icon: 'mdi-map-marker-distance', disabled: true},
      {name: 'Clustering Jerárquico', route: '/clustering-jerarquico', icon: 'mdi-graph', disabled: true},
      {name: 'Clustering Particional', route: '/clustering-particional', icon: 'mdi-grain', disabled: true},
      {name: 'Regresión Logística', route: '/regresion-logistica', icon: 'mdi-chart-bell-curve-cumulative', disabled: false},
    ],
    dialog: false,
  }),
  methods: {
    ...mapActions(["uploadFile", "getHeaders", "getTable"]),
    ...mapMutations(["reset"]),
    async cargarArchivo(){
      this.dialog = false;
      if(this.file){
        this.overlay = true;
        await this.uploadFile({file: this.file, header: this.header});
        await this.getHeaders();
        await this.getTable();
        this.overlay = false;
        this.itemAppBar.map((item) => {
          item.disabled =  false;
        });
      }else
        this.reset();
    },
    updateFile(){
      if(!this.file)
        this.itemAppBar.map((item) => {
          item.disabled =  true;
        });
    }
  },
  computed: {
    ...mapState(["headers"]),
  },
  validations:{
    file: {required}
  },
  mounted() {
    this.$router.push("/")
  },
};
</script>