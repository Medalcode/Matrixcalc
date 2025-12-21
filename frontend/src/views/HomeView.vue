<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const router = useRouter()

const goToCalculator = () => {
  router.push('/calculator')
}
</script>

<template>
  <div class="py-12">
    <!-- Hero Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center">
        <div class="flex justify-center mb-8">
          <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center text-white font-bold text-4xl shadow-2xl">
            M
          </div>
        </div>
        <h1 class="text-4xl font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
          {{ t('home.title') }}
        </h1>
        <p class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
          {{ t('home.subtitle') }}
        </p>
        <div class="mt-8 flex justify-center gap-4">
          <button
            @click="goToCalculator"
            class="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-lg hover:bg-blue-700 transition-colors"
          >
            {{ t('home.cta.start') }}
          </button>
          <router-link
            to="/about"
            class="px-8 py-3 bg-white text-blue-600 font-semibold rounded-lg shadow-lg border-2 border-blue-600 hover:bg-blue-50 transition-colors"
          >
            {{ t('home.cta.learnMore') }}
          </router-link>
        </div>
      </div>

      <!-- Features -->
      <div class="mt-20">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">
          {{ t('home.features.title') }}
        </h2>
        <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <!-- Operaciones -->
          <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              {{ t('home.features.operations') }}
            </h3>
            <p class="text-gray-600 text-sm">
              {{ t('home.features.operationsDesc') }}
            </p>
          </div>

          <!-- Historial -->
          <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              {{ t('home.features.history') }}
            </h3>
            <p class="text-gray-600 text-sm">
              {{ t('home.features.historyDesc') }}
            </p>
          </div>

          <!-- Import/Export -->
          <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              {{ t('home.features.export') }}
            </h3>
            <p class="text-gray-600 text-sm">
              {{ t('home.features.exportDesc') }}
            </p>
          </div>

          <!-- Estadísticas -->
          <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              {{ t('home.features.stats') }}
            </h3>
            <p class="text-gray-600 text-sm">
              {{ t('home.features.statsDesc') }}
            </p>
          </div>
        </div>
      </div>

      <!-- Visual Demo -->
      <div class="mt-20 bg-white rounded-2xl shadow-2xl p-8 md:p-12">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div>
            <h3 class="text-2xl font-bold text-gray-900 mb-4">
              Potente y Preciso
            </h3>
            <p class="text-gray-600 mb-6">
              Realiza cálculos matriciales con precisión de punto flotante de 64 bits usando NumPy.
              Soporta matrices de hasta 1000x1000 elementos con tiempos de respuesta instantáneos.
            </p>
            <ul class="space-y-3">
              <li class="flex items-start gap-3">
                <svg class="w-6 h-6 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <span class="text-gray-700">Cálculos precisos con NumPy</span>
              </li>
              <li class="flex items-start gap-3">
                <svg class="w-6 h-6 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <span class="text-gray-700">Interfaz intuitiva y responsive</span>
              </li>
              <li class="flex items-start gap-3">
                <svg class="w-6 h-6 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <span class="text-gray-700">Soporte para CSV y JSON</span>
              </li>
            </ul>
          </div>
          <div class="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-8">
            <div class="font-mono text-sm space-y-2">
              <div class="bg-white rounded p-3 shadow">
                <span class="text-gray-500">// Matriz A</span><br>
                <span class="text-blue-600">[1, 2, 3]</span><br>
                <span class="text-blue-600">[4, 5, 6]</span>
              </div>
              <div class="text-center text-2xl text-gray-400">×</div>
              <div class="bg-white rounded p-3 shadow">
                <span class="text-gray-500">// Matriz B</span><br>
                <span class="text-purple-600">[7, 8]</span><br>
                <span class="text-purple-600">[9, 10]</span><br>
                <span class="text-purple-600">[11, 12]</span>
              </div>
              <div class="text-center text-2xl text-gray-400">=</div>
              <div class="bg-white rounded p-3 shadow border-2 border-green-500">
                <span class="text-gray-500">// Resultado</span><br>
                <span class="text-green-600">[58, 64]</span><br>
                <span class="text-green-600">[139, 154]</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
