<template>
  <div id="card">
    <vocabgrid></vocabgrid>
  </div>
</template>

<script>
import vocabgrid from '@/components/vocab-grid.vue';

  export default {
    name: 'Hola',
    components:{
      vocabgrid,
    },
    data: () => ({
      activeSquare: 0
    }),
    methods: {
      onClickSquare (x){
        this.activeSquare = x;
      }
    }
  }
</script>
