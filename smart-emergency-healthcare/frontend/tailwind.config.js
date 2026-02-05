/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0f172a", // Slate 900
        surface: "#1e293b", // Slate 800
        primary: "#3b82f6", // Blue 500
        secondary: "#ec4899", // Pink 500
        accent: "#8b5cf6", // Violet 500
        success: "#10b981", // Emerald 500
        warning: "#f59e0b", // Amber 500
        danger: "#ef4444", // Red 500
      },
      animation: {
        blob: "blob 7s infinite",
      },
      keyframes: {
        blob: {
          "0%": { transform: "translate(0px, 0px) scale(1)" },
          "33%": { transform: "translate(30px, -50px) scale(1.1)" },
          "66%": { transform: "translate(-20px, 20px) scale(0.9)" },
          "100%": { transform: "translate(0px, 0px) scale(1)" },
        },
      },
    },
  },
  plugins: [],
}
