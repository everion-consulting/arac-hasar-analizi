import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite config:
// - Uygulama kökte (/ ) çalışır, base tanımlamıyoruz.
// - Nginx, prod'da domain kökünü Vite'e (5173) proxy'ler.

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    allowedHosts: ['hasar.everionai.com', 'localhost', '127.0.0.1'],
    proxy: {
      '/predict': 'http://localhost:8000',
      '/auth': 'http://localhost:8000',
      '/api': 'http://localhost:8000',
    },
    watch: {
      ignored: ['**/backend/**', '**/node_modules/**', '**/.git/**', '**/django_arac_hasar_backend/**'],
    },
  },
})

