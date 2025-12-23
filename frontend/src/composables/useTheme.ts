import { ref, watch, onMounted } from 'vue'

export type Theme = 'light' | 'dark' | 'auto'

const STORAGE_KEY = 'matrixcalc-theme'

const theme = ref<Theme>('auto')
const isDark = ref(false)

export function useTheme() {
  const setTheme = (newTheme: Theme) => {
    theme.value = newTheme
    localStorage.setItem(STORAGE_KEY, newTheme)
    applyTheme()
  }
  
  const applyTheme = () => {
    if (theme.value === 'dark' || 
        (theme.value === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark')
      isDark.value = true
    } else {
      document.documentElement.classList.remove('dark')
      isDark.value = false
    }
  }
  
  const toggleTheme = () => {
    if (theme.value === 'light') {
      setTheme('dark')
    } else if (theme.value === 'dark') {
      setTheme('auto')
    } else {
      setTheme('light')
    }
  }
  
  const initTheme = () => {
    // Load theme from localStorage
    const stored = localStorage.getItem(STORAGE_KEY) as Theme | null
    if (stored && ['light', 'dark', 'auto'].includes(stored)) {
      theme.value = stored
    }
    
    applyTheme()
    
    // Watch for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', () => {
      if (theme.value === 'auto') {
        applyTheme()
      }
    })
  }
  
  // Watch for theme changes
  watch(theme, applyTheme)
  
  return {
    theme,
    isDark,
    setTheme,
    toggleTheme,
    initTheme
  }
}
