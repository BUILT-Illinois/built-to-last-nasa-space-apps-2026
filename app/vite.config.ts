// Vite config for the web app. Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
});
