import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

const isDev = process.env.NODE_ENV !== 'production'
const port = process.env.VUE_PORT !== undefined ? process.env.VUE_PORT : 5173
console.log(isDev)
console.log(`VUE_PORT: ${port}`)
export default defineConfig({
  plugins: [
    vue(),
    isDev && vueDevTools(),
    tailwindcss(),
  ].filter(Boolean),
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: isDev ? {
    watch: {
      usePolling: true,
    },
    port: port,
    host: true,
  } : undefined
})
