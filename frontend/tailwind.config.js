/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        neon: "#00f6ff",
        darkbg: "#0b0f19",
      },
    },
  },
  plugins: [],
}
