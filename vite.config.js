import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/static/', 
  server: {
    proxy: {
      '/predict': 'http://localhost:8000',
    },
    watch: {
      ignored: ['**/backend/**', '**/node_modules/**', '**/.git/**', '**/django_arac_hasar_backend/**'],
    },
  },
})