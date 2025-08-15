// frontend/tailwind.config.ts

import type { Config } from "tailwindcss";

const config = {
  // If you already have a darkMode key, replace it. If not, add it.
  darkMode: ["class"], 
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  // ... rest of your config
} satisfies Config;

export default config;