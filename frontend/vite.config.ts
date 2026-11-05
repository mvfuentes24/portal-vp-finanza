import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// En desarrollo, las peticiones a /api se reenvían al backend (FastAPI).
// Para el navegador, frontend y API comparten origen: la cookie de sesión
// funciona sin configuraciones adicionales de CORS.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
