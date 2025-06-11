/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue"
  ],
  theme: {
    extend: {
      fontFamily: {
        'multilingual': [
          'Inter', 
          'Noto Sans CJK TC', 
          'Noto Sans CJK JP', 
          'Hiragino Sans', 
          'Yu Gothic UI', 
          'Meiryo', 
          'MS Gothic',
          '-apple-system', 
          'BlinkMacSystemFont', 
          'sans-serif'
        ],
      },
      colors: {
        // 新的現代化配色方案
        'neon': {
          'blue': '#00D2FF',
          'purple': '#B537F2', 
          'green': '#00F5A0',
          'pink': '#FF006E',
          'orange': '#FB8500',
          'yellow': '#FFD60A'
        },
        'dark': {
          'primary': '#0a0a0a',
          'secondary': '#0f0f0f',
          'tertiary': '#1a0a2e',
          'surface': '#16213e',
          'card': 'rgba(20, 20, 30, 0.95)',
          'glass': 'rgba(15, 15, 25, 0.8)',
          'border': 'rgba(255, 255, 255, 0.1)',
          'border-hover': 'rgba(0, 210, 255, 0.5)'
        },
        'text': {
          'primary': '#ffffff',
          'secondary': '#e2e8f0',
          'muted': '#94a3b8',
          'accent': '#00D2FF'
        },
        // 為了確保所有背景色變體可用
        'bg-neon-blue': '#00D2FF',
        'bg-neon-purple': '#B537F2',
        'bg-neon-pink': '#FF006E',
        'bg-neon-green': '#00F5A0',
        'bg-neon-yellow': '#FFD60A'
      },
      animation: {
        'fade-in': 'fadeIn 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards',
        'slide-up': 'slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards',
        'scale-in': 'scaleIn 0.3s cubic-bezier(0.4, 0, 0.2, 1) forwards',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite alternate',
        'bounce-gentle': 'bounceGentle 0.6s ease-out',
        'shimmer': 'shimmer 2s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
        'glow-pulse': 'glowPulse 2s ease-in-out infinite alternate',
        'slide-left': 'slideLeft 0.3s ease-out',
        'slide-right': 'slideRight 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          'from': { opacity: '0', transform: 'translateY(10px)' },
          'to': { opacity: '1', transform: 'translateY(0)' }
        },
        slideUp: {
          'from': { 
            opacity: '0',
            transform: 'translateY(30px) scale(0.95)'
          },
          'to': {
            opacity: '1',
            transform: 'translateY(0) scale(1)'
          }
        },
        scaleIn: {
          'from': {
            opacity: '0',
            transform: 'scale(0.9)'
          },
          'to': {
            opacity: '1',
            transform: 'scale(1)'
          }
        },
        pulseGlow: {
          'from': { boxShadow: '0 0 20px rgba(0, 210, 255, 0.3)' },
          'to': { boxShadow: '0 0 30px rgba(181, 55, 242, 0.6)' }
        },
        bounceGentle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' }
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-6px)' }
        },
        glowPulse: {
          'from': { boxShadow: '0 0 20px rgba(0, 210, 255, 0.4), 0 0 40px rgba(181, 55, 242, 0.2)' },
          'to': { boxShadow: '0 0 30px rgba(181, 55, 242, 0.6), 0 0 60px rgba(0, 210, 255, 0.3)' }
        },
        slideLeft: {
          'from': { transform: 'translateX(100%)', opacity: '0' },
          'to': { transform: 'translateX(0)', opacity: '1' }
        },
        slideRight: {
          'from': { transform: 'translateX(-100%)', opacity: '0' },
          'to': { transform: 'translateX(0)', opacity: '1' }
        }
      },
      backdropBlur: {
        'xs': '2px',
        '10': '10px',
        '15': '15px',
        '25': '25px',
      },
      boxShadow: {
        'glow-blue': '0 0 20px rgba(0, 210, 255, 0.5)',
        'glow-purple': '0 0 20px rgba(181, 55, 242, 0.5)',
        'glow-green': '0 0 20px rgba(0, 245, 160, 0.5)',
        'card-hover': '0 20px 40px rgba(0, 0, 0, 0.3), 0 0 30px rgba(0, 210, 255, 0.2)',
        'neon': '0 0 5px currentColor, 0 0 20px currentColor, 0 0 35px currentColor',
      },
      zIndex: {
        '45': '45',
      }
    },
  },
  plugins: [],
}