/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // "Light and Dynamic" color palette
      colors: {
        'background': '#F5F5F5', // A clean, very light gray
        'surface': '#FFFFFF',    // Pure white for cards and surfaces
        'primary': '#FF5722',    // A vibrant, dynamic orange
        'text-main': '#121212',  // A dark charcoal for high contrast
        'text-secondary': '#757575', // A medium gray for secondary text
      },
      fontFamily: {
        sans: ['Sora', 'sans-serif'],
      },
    },
  },
  plugins: [],
}