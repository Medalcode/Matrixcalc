import { createI18n } from 'vue-i18n'
import es from './locales/es'
import en from './locales/en'

// Detectar el idioma del navegador
const getBrowserLocale = (): string => {
  const navigatorLocale = navigator.language || (navigator as any).userLanguage
  
  if (!navigatorLocale) {
    return 'es'
  }
  
  // Obtener solo el código del idioma (ej: 'es-CL' -> 'es')
  const locale = navigatorLocale.trim().split(/-|_/)[0]
  
  // Idiomas soportados
  const supportedLocales = ['es', 'en']
  
  // Si el idioma está soportado, usarlo; sino, español por defecto
  return supportedLocales.includes(locale) ? locale : 'es'
}

// Guardar/recuperar idioma del localStorage
const getStoredLocale = (): string => {
  const stored = localStorage.getItem('matrixcalc-locale')
  return stored || getBrowserLocale()
}

const i18n = createI18n({
  legacy: false, // Usar Composition API
  locale: getStoredLocale(),
  fallbackLocale: 'es',
  messages: {
    es,
    en,
  },
})

// Función helper para cambiar idioma
export const setLocale = (locale: string) => {
  i18n.global.locale.value = locale as any
  localStorage.setItem('matrixcalc-locale', locale)
  document.querySelector('html')?.setAttribute('lang', locale)
}

// Establecer el atributo lang en el HTML
document.querySelector('html')?.setAttribute('lang', getStoredLocale())

export default i18n
