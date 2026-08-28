import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
import tailwindcss from "@tailwindcss/vite";
export default defineConfig({
  root: "client",
  plugins: [react(), tailwindcss()],
  resolve: { alias: { "@": path.resolve(__dirname, "client/src"), "@shared": path.resolve(__dirname, "shared") } },
  build: {
    outDir: path.resolve(__dirname, "dist/public"),
    emptyOutDir: true,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes("node_modules")) return;
          if (id.includes("react-dom") || id.includes("/react/") || id.includes("scheduler")) return "vendor-react";
          if (id.includes("@tanstack") || id.includes("@trpc") || id.includes("superjson")) return "vendor-data";
          if (id.includes("lucide-react")) return "vendor-icons";
          if (id.includes("appwrite")) return "vendor-appwrite";
          if (id.includes("framer-motion") || id.includes("embla-carousel") || id.includes("recharts") || id.includes("react-day-picker")) return "vendor-ui";
          return "vendor-core";
        },
      },
    },
  },
  server: { port: 5173, host: "0.0.0.0", allowedHosts: true },
});
