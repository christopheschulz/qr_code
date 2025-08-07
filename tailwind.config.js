/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/QrCodeReader/templates/**/*.html",
    "./src/QrCodeReader/static/**/*.js",
    "./src/**/*.py",
  ],
  safelist: [
    'active',
    'hidden',
    'bg-blue-500',
    'bg-blue-600', 
    'text-white',
    'border-blue-500'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}