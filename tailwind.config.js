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
    'border-blue-500',
    'max-h-0',
    'max-h-screen',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      keyframes: {
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'scale-in': {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },
      animation: {
        'fade-in-up': 'fade-in-up 0.4s ease-out',
        'scale-in': 'scale-in 0.3s ease-out',
      },
    },
  },
  plugins: [],
}
