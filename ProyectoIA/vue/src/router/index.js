import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/datos',
    name: 'Datos',
    component: () => import('../views/Datos.vue')
  },
  {
    path: '/asociacion',
    name: 'Asociacion',
    component: () => import('../views/Asociacion.vue')
  },
  {
    path: '/correlacional',
    name: 'Correlacional',
    component: () => import('../views/Correlacional.vue')
  },
  {
    path: '/distancias',
    name: 'Distancias',
    component: () => import('../views/Distancias.vue')
  },
  {
    path: '/clustering-particional',
    name: 'ClusteringParticional',
    component: () => import('../views/ClusteringParticional.vue')
  },
  {
    path: '/clustering-jerarquico',
    name: 'ClusteringJerarquico',
    component: () => import('../views/ClusteringJerarquico.vue')
  },
  {
    path: '/regresion-logistica',
    name: 'RegLogistica',
    component: () => import('../views/RegLogistica.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
