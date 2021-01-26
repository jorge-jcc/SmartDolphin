<template>
  <v-container fluid>   
    <v-card class="px-2 py-3" height='100%'>
      <p class="text-h4 ">Diagnóstico de Tumores</p>
      <v-row class="mx-10" justify="center" align="center">
        <v-col cols="8">
          <p class="text-h6">Datos Personales</p>
          <v-row>
            <v-col cols="12" sm="3" class="my-0 py-0">
              <v-text-field dense label="ID"/>
            </v-col>
            <v-col cols="12" sm="9" class="my-0 py-0">
              <v-text-field dense label="Nombre"/>
            </v-col>
            <v-col cols="12" sm="6" class="my-0 py-0">
              <v-text-field dense label="Apellido Paterno"/>
            </v-col>
            <v-col cols="12" sm="6" class="my-0 py-0">
              <v-text-field dense label="Apellido Materno"/>
            </v-col>
          </v-row>
          <p class="text-h6">Estudios Realizados*</p>
          <v-row>
            <v-col cols="12" class="my-0 py-0">
              <v-alert dense text type="error" v-model="maligno">
                <strong>Diagnóstico:</strong> Posible Tumor Maligno
              </v-alert>
            </v-col>
            <v-col cols="12" class="my-0 py-0">
              <v-alert dense text type="info" v-model="benigno">
                <strong>Diagnóstico:</strong> Posible Tumor Benigno
              </v-alert>
            </v-col>
            <v-col cols="12" sm="4" class="mb-1 py-0">
              <v-text-field v-model="$v.form.texture.$model"
                :error-messages="textureErrors"
                dense label="Textura"/>
            </v-col>
            <v-col cols="12" sm="4" class="mb-1 py-0">
              <v-text-field v-model="$v.form.area.$model"
                :error-messages="areaErrors"
                dense label="Area"/>
            </v-col>
            <v-col cols="12" sm="4" class="mb-1 py-0">
              <v-text-field v-model="$v.form.compactness.$model"
                :error-messages="compactnessErrors"
                dense label="Compactness"/>
            </v-col>
            <v-col cols="12" sm="4" class="my-0 py-0">
              <v-text-field  v-model="$v.form.concavity.$model"
                :error-messages="concavityErrors"
                dense label="Concavity"/>
            </v-col>
            <v-col cols="12" sm="4" class="my-0 py-0">
              <v-text-field  v-model="$v.form.symmetry.$model"
                :error-messages="symmetryErrors"
                dense label="Symmetry"/>
            </v-col>
            <v-col cols="12" sm="4" class="my-0 py-0">
              <v-text-field  v-model="$v.form.fractalDimension.$model"
                :error-messages="fractalDimensionErrors"
                dense label="FractalDimension"/>
            </v-col>
            <!--:disabled="$v.form.$invalid"-->
            <v-col class="my-0 py-0">
              <v-btn right color="primary" @click="getResultados" :disabled="$v.form.$invalid">
                <v-icon left dark>mdi-cog</v-icon>
                Analizar Datos
              </v-btn>
              <v-btn right dark color="red darken-1" @click="cleanForm" class="ml-3">
                <v-icon left dark>mdi-broom</v-icon>
                Limpiar
              </v-btn>
            </v-col>
            <v-col justify="end" class="my-0 py-0">
              
            </v-col>
          </v-row>
          <v-row class="mt-4 ml-0">
            <p class="text-caption"><span class="font-weight-bold">*Exactitud:</span> 0.9298245614035088</p>
          </v-row>
        </v-col>
        <v-col cols="3">
          <v-img src="../assets/medicina.png"></v-img>
        </v-col>
      </v-row>
    </v-card>

  </v-container>
</template>

<script>
import { required, decimal, numeric } from 'vuelidate/lib/validators';
import { validationMixin } from 'vuelidate';


export default {
  name: 'Asociacion',
  data() {
    return {
      form:{
        texture: null,
        area : null,
        compactness: null,
        concavity: null,
        symmetry: null,
        fractalDimension: null
      },
      dialog : false,
      maligno: false,
      benigno: false,
    }
  },
  validations: {
    form:{
      texture: { required, decimal},
      area: { required, decimal },
      compactness: { required, decimal },
      concavity: { required, decimal },
      symmetry: { required, decimal },
      fractalDimension: { required, decimal }
    },
  },
  computed: {
    textureErrors(){
      const errors = []
      if (!this.$v.form.texture.$dirty) return errors
      !this.$v.form.texture.decimal && errors.push('Formato incorrecto')
      !this.$v.form.texture.required && errors.push('Se requiere algún valor')
      return errors
    },
    areaErrors(){
      const errors = []
      if (!this.$v.form.area.$dirty) return errors
      !this.$v.form.area.decimal && errors.push('Formato incorrecto')
      !this.$v.form.area.required && errors.push('Se requiere algún valor')
      return errors
    },
    compactnessErrors(){
      const errors = []
      if (!this.$v.form.compactness.$dirty) return errors
      !this.$v.form.compactness.decimal && errors.push('Formato incorrecto')
      !this.$v.form.compactness.required && errors.push('Se requiere algún valor')
      return errors
    },
    concavityErrors(){
      const errors = []
      if (!this.$v.form.concavity.$dirty) return errors
      !this.$v.form.concavity.decimal && errors.push('Formato incorrecto')
      !this.$v.form.concavity.required && errors.push('Se requiere algún valor')
      return errors
    },
    symmetryErrors(){
      const errors = []
      if (!this.$v.form.symmetry.$dirty) return errors
      !this.$v.form.symmetry.decimal && errors.push('Formato incorrecto')
      !this.$v.form.symmetry.required && errors.push('Se requiere algún valor')
      return errors
    },
    fractalDimensionErrors(){
      const errors = []
      if (!this.$v.form.fractalDimension.$dirty) return errors
      !this.$v.form.fractalDimension.decimal && errors.push('Formato incorrecto')
      !this.$v.form.fractalDimension.required && errors.push('Se requiere algún valor')
      return errors
    },
  },
  methods: {
    getResultados(){
      this.benigno = false;
      this.maligno = false;
      const promise = new Promise((resolve, reject) => {
        eel.get_regresion_logistica(
          this.$v.form.texture.$model,
          this.$v.form.area.$model,
          this.$v.form.compactness.$model,
          this.$v.form.concavity.$model,
          this.$v.form.symmetry.$model,
          this.$v.form.fractalDimension.$model
        )((response) => {
          resolve(response);
        });
      });
      promise.then((response) => {
        this.benigno = response == 1 ? true : false;
        this.maligno = !this.benigno;
      });
    },
    cleanForm(){
      this.benigno = false;
      this.maligno = false;
      this.$v.form.texture.$model = null;
      this.$v.form.area.$model = null;
      this.$v.form.compactness.$model = null;
      this.$v.form.concavity.$model = null;
      this.$v.form.symmetry.$model = null;
      this.$v.form.fractalDimension.$model = null;
      this.$v.$reset();
    }
  },
  mounted() {
    this.maligno = false;
    this.benigno = false;
  },
}
</script>
