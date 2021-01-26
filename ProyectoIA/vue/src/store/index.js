import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    table: null,
    file: null,
    headers: null,
  },
  mutations: {
    setTable(state, payload){
      state.table = payload.table;
    },
    setHeaders(state, payload){
      state.headers = payload.headers;
    },
    setTable(state, payload){
      state.table = payload.table;
    },
    reset(state){
      state.table = null;
      state.headers = null;
    }
  },
  actions: {
    uploadFile({commit}, payload){
      return new Promise((resolve, reject) => {
        if(payload.file){
          const reader = new FileReader();
          console.log(payload.file)
          reader.readAsText(payload.file);
          reader.onload = () => {
            eel.load_file(reader.result, payload.file.name, payload.header);
            resolve(reader.result);
          }
        }
      });
    },
    getHeaders({commit}){
      return new Promise((resolve, reject) => {
        eel.get_headers()((response) => {
          commit('setHeaders', {headers : response})
          resolve(response);
        });
      });
    },
    getTable({commit}){
      return new Promise((resolve, reject) => {
        eel.get_table()((response) => {
          commit('setTable', {table : response})
          resolve(response);
        });
      });
    }
  },
  modules: {
  }
})
