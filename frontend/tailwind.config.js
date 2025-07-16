/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'serif': ['Georgia', 'serif'],
        'display': ['Playfair Display', 'Georgia', 'serif'],
      },
      colors: {
        'parchment': '#f7f3e9',
        'ink': '#2c1810',
        'gold': '#d4af37',
        'mahogany': '#8b4513',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
