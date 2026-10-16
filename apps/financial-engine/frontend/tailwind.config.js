/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        bank: {
          void: "#0a0b0d",
          abyss: "#0f1115",
          slate: "#161920",
          graphite: "#1c1f27",
          steel: "#252932",
          mist: "#2e3340",
          platinum: "#c8cdd6",
          silver: "#9aa3b2",
          muted: "#6b7280",
          gold: {
            50: "#fbf6e9",
            100: "#f5ebd0",
            200: "#ead9a3",
            300: "#dcc46e",
            400: "#c9a94a",
            500: "#b8923a",
            600: "#9a7530",
            700: "#7a5c28",
            800: "#644b24",
            900: "#543f21",
          },
          accent: "#d4af37",
          success: "#3d9a6a",
          danger: "#c45c5c",
          info: "#5b8def",
        },
      },
      fontFamily: {
        display: ["'Cormorant Garamond'", "Georgia", "serif"],
        sans: ["'Inter'", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "ui-monospace", "monospace"],
      },
      backgroundImage: {
        "premium-radial":
          "radial-gradient(ellipse 80% 50% at 50% -20%, rgba(184, 146, 58, 0.12), transparent)",
        "premium-fade":
          "linear-gradient(180deg, #0f1115 0%, #0a0b0d 40%, #0a0b0d 100%)",
        "card-sheen":
          "linear-gradient(135deg, rgba(255,255,255,0.04) 0%, transparent 50%, rgba(212,175,55,0.03) 100%)",
        "gold-degrade":
          "linear-gradient(135deg, #d4af37 0%, #b8923a 40%, #7a5c28 100%)",
        "surface-degrade":
          "linear-gradient(160deg, #1c1f27 0%, #161920 55%, #0f1115 100%)",
      },
      boxShadow: {
        panel: "0 0 0 1px rgba(255,255,255,0.04), 0 8px 32px rgba(0,0,0,0.45)",
        "panel-hover":
          "0 0 0 1px rgba(212,175,55,0.18), 0 12px 40px rgba(0,0,0,0.55)",
        glow: "0 0 24px rgba(212,175,55,0.15)",
      },
      animation: {
        "fade-in": "fadeIn 0.5s ease-out",
        "slide-up": "slideUp 0.45s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
