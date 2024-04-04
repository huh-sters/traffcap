import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { Quasar } from 'quasar'

// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'

import 'quasar/dist/quasar.css'

const app = createApp(App)

app.use(router)
app.use(Quasar, {
    plugins: {},
})

app.mount('#app')
