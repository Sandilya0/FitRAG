/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: '#F8F9FA',
        card: '#FFFFFF',
        ink: '#0D0D0D',
        muted: '#8A8A8A',
        line: '#ECECEC',
        good: '#00C878',
        amber: '#F5A623',
        low: '#E53935',
        accent: '#1A73E8',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['"DM Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}