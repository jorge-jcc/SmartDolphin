<template>
  <v-container fluid>
    <v-overlay :value="loading" z-index="0" absolute>
      <v-progress-circular indeterminate color="purple" size="64"></v-progress-circular>
    </v-overlay>

    <p class="text-h4">Configuración de Parámetros</p>
    <v-row justify="center" class="mx-2">
      <v-col cols="6">
        <v-text-field v-model="$v.form.support.$model"
          :error-messages="supportErrors"
          label="Soporte Mínimo"
          class="mx-2 my-0">
        </v-text-field>
        <v-text-field v-model="$v.form.confidence.$model"
          :error-messages="confidenceErrors"
          label="Confianza Mínima"
          class="mx-2 my-0">
        </v-text-field>
        <v-text-field v-model="$v.form.lift.$model"
          :error-messages="liftErrors"
          label="Elevación"
          class="mx-2 my-0">
        </v-text-field>
        <v-text-field v-model="$v.form.length.$model"
          :error-messages="lengthErrors"
          label="Mínimo de elementos"
          class="mx-2 my-0">
        </v-text-field>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="6">
        <v-row justify="end" class="mr-5">
          <v-btn right color="primary" class="white--text" @click="getApriori"
            :disabled="$v.form.$invalid">
            <v-icon left dark>mdi-cog</v-icon>
            Procesar
          </v-btn>
        </v-row>
      </v-col>
    </v-row>
    <v-divider class="my-2"></v-divider>
    <p class="text-h4" v-if="apriori">Reglas de Asociación</p>
    <v-data-table v-if="apriori"
      dense
      :headers="headers"
      :items="apriori"
      item-key="name"
      class="elevation-1">
    </v-data-table>
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
        support: 0.0045,
        confidence : 0.2,
        lift: 3,
        length: 2,
      },
      loading : false,
      apriori : null,
      headers: [
        {
          text: 'Antecedente',
          align: 'start',
          sortable: false,
          value: 'items_base',
        },
        {
          text: 'Consecuente',
          align: 'start',
          sortable: false,
          value: 'items_add',
        },
        { text: 'Confianza', value: 'confidence' },
        { text: 'Soporte', value: 'support' },
        { text: 'Lift', value: 'lift' },
      ],
    }
  },
  validations: {
    form:{
      support: { required, decimal},
      confidence: { required, decimal },
      lift: { required, decimal },
      length: { required, numeric }
    },
  },
  computed: {
    supportErrors(){
      const errors = []
      if (!this.$v.form.support.$dirty) return errors
      !this.$v.form.support.decimal && errors.push('Formato incorrecto')
      !this.$v.form.support.required && errors.push('Se requiere algún valor')
      return errors
    },
    confidenceErrors(){
      const errors = []
      if (!this.$v.form.confidence.$dirty) return errors
      !this.$v.form.confidence.decimal && errors.push('Formato incorrecto')
      !this.$v.form.confidence.required && errors.push('Se requiere algún valor')
      return errors
    },
    liftErrors(){
      const errors = []
      if (!this.$v.form.lift.$dirty) return errors
      !this.$v.form.lift.decimal && errors.push('Formato incorrecto')
      !this.$v.form.lift.required && errors.push('Se requiere algún valor')
      return errors
    },
    lengthErrors(){
      const errors = []
      if (!this.$v.form.length.$dirty) return errors
      !this.$v.form.length.numeric && errors.push('Formato incorrecto')
      !this.$v.form.length.required && errors.push('Se requiere algún valor')
      return errors
    },
  },
  methods: {
    getApriori(){
      this.loading = true;
      this.apriori = null;
      const promise = new Promise((resolve, reject) => {
        eel.get_apriori(
          this.$v.form.support.$model,
          this.$v.form.confidence.$model,
          this.$v.form.lift.$model,
          this.$v.form.length.$model
        )((response) => {
          this.apriori = response;
          resolve(response);
        });
      });
      promise.then((response) => {this.loading = false});
    }
  },
}
</script>
