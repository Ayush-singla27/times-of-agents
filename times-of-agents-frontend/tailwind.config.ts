import type { Config } from "tailwindcss";


const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        charcoal: "#1C1C1E",
        "off-white": "#F8F7F4",
        "card-white": "#FFFFFF",
        muted: "#6B6B70",
        "analytical-blue": "#2563EB",
        "conflict-red": "#B83A2E",
        "insight-amber": "#D97706",
        "accent-purple": "#7C3AED",
        "accent-green": "#059669",
        "ap-border": "#E5E3DC",
        emotion: {
          joy: "#F59E0B",
          trust: "#10B981",
          fear: "#6366F1",
          surprise: "#EC4899",
          sadness: "#64748B",
          disgust: "#84CC16",
          anger: "#EF4444",
          anticipation: "#F97316",
        },
      },
      fontFamily: {
        playfair: ["var(--font-playfair)", "Georgia", "serif"],
        inter: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
