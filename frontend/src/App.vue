<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { setLocale } from './i18n'

const { t, locale } = useI18n()

const changeLocale = (newLocale: string) => {
  setLocale(newLocale)
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Navegación -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo y nombre -->
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-xl shadow-lg">
              M
            </div>
            <span class="text-xl font-bold text-gray-900">MatrixCalc</span>
          </div>

          <!-- Links de navegación -->
          <div class="hidden md:flex items-center gap-1">
            <RouterLink
              to="/"
              class="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 hover:text-blue-600 transition-colors font-medium"
              active-class="bg-blue-50 text-blue-600"
            >
              {{ t('nav.home') }}
            </RouterLink>
            <RouterLink
              to="/calculator"
              class="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 hover:text-blue-600 transition-colors font-medium"
              active-class="bg-blue-50 text-blue-600"
            >
              {{ t('nav.calculator') }}
            </RouterLink>
            <RouterLink
              to="/stats"
              class="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 hover:text-blue-600 transition-colors font-medium"
              active-class="bg-blue-50 text-blue-600"
            >
              {{ t('nav.stats') }}
            </RouterLink>
            <RouterLink
              to="/about"
              class="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 hover:text-blue-600 transition-colors font-medium"
              active-class="bg-blue-50 text-blue-600"
            >
              {{ t('nav.about') }}
            </RouterLink>
          </div>

          <!-- Selector de idioma -->
          <div class="flex items-center gap-2">
            <button
              @click="changeLocale('es')"
              :class="[
                'px-3 py-1.5 rounded-md text-sm font-medium transition-colors',
                locale === 'es'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              ES
            </button>
            <button
              @click="changeLocale('en')"
              :class="[
                'px-3 py-1.5 rounded-md text-sm font-medium transition-colors',
                locale === 'en'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              EN
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Contenido principal -->
    <main class="flex-grow">
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="text-center text-gray-600 text-sm">
          <p>MatrixCalc © {{ new Date().getFullYear() }} - Calculadora de Matrices Profesional</p>
          <p class="mt-1">
            Desarrollado con
            <span class="text-red-500">❤</span>
            usando Vue.js, Django y NumPy
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
main {
  min-height: calc(100vh - 64px - 88px);
}
</style>
