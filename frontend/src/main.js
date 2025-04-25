import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import piniaPersistedState from 'pinia-plugin-persistedstate'

import "bootstrap"
import "bootstrap/dist/css/bootstrap.min.css"
import 'bootstrap-icons/font/bootstrap-icons.css'

const app = createApp(App)

// const pinia = createPinia()

// pinia.use((context) => {
//   if (typeof context.store.loadFromStorage === 'function') {
//     context.store.loadFromStorage()
//   }
// })


const pinia = createPinia()
pinia.use(piniaPersistedState)

app.use(pinia)
app.use(router)

app.mount('#app')
