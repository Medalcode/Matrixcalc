<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="py-12 bg-gray-50 dark:bg-gray-900 min-h-screen transition-colors duration-200">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="text-center mb-12">
        <div class="flex justify-center mb-6">
          <div class="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center text-white font-bold text-3xl shadow-2xl">
            M
          </div>
        </div>
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          {{ t('about.title') }}
        </h1>
        <p class="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
          {{ t('about.description') }}
        </p>
        <div class="mt-4">
          <span class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">
            {{ t('about.version') }} 2.0.0
          </span>
        </div>
      </div>

      <!-- Features -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8 border border-gray-200 dark:border-gray-700 transition-colors duration-200">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          {{ t('about.features.title') }}
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="flex items-start gap-3">
            <svg class="w-6 h-6 text-green-500 dark:text-green-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            <span class="text-gray-700 dark:text-gray-300">{{ t('about.features.feature1') }}</span>
          </div>
          <div class="flex items-start gap-3">
            <svg class="w-6 h-6 text-green-500 dark:text-green-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            <span class="text-gray-700 dark:text-gray-300">{{ t('about.features.feature2') }}</span>
          </div>
          <div class="flex items-start gap-3">
            <svg class="w-6 h-6 text-green-500 dark:text-green-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            <span class="text-gray-700 dark:text-gray-300">{{ t('about.features.feature3') }}</span>
          </div>
          <div class="flex items-start gap-3">
            <svg class="w-6 h-6 text-green-500 dark:text-green-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            <span class="text-gray-700 dark:text-gray-300">{{ t('about.features.feature4') }}</span>
          </div>
          <div class="flex items-start gap-3">
            <svg class="w-6 h-6 text-green-500 dark:text-green-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            <span class="text-gray-700 dark:text-gray-300">{{ t('about.features.feature5') }}</span>
          </div>
          <div class="flex items-start gap-3">
            <svg class="w-6 h-6 text-green-500 dark:text-green-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            <span class="text-gray-700 dark:text-gray-300">{{ t('about.features.feature6') }}</span>
          </div>
        </div>
      </div>

      <!-- Tech Stack -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8 border border-gray-200 dark:border-gray-700 transition-colors duration-200">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          {{ t('about.tech.title') }}
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Frontend -->
          <div class="text-center">
            <div class="w-16 h-16 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center mx-auto mb-3">
              <svg class="w-10 h-10 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0l-11 3v12.58c0 6.33 4.38 11.87 11 13.42 6.62-1.55 11-7.09 11-13.42v-12.58l-11-3zm0 2.18l9 2.45v10.95c0 5.42-3.78 10.22-9 11.6-5.22-1.38-9-6.18-9-11.6v-10.95l9-2.45z"/>
              </svg>
            </div>
            <h3 class="font-semibold text-gray-900 dark:text-white mb-2">{{ t('about.tech.frontend') }}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">Vue.js 3, TypeScript, Tailwind CSS, Pinia, Chart.js</p>
          </div>

          <!-- Backend -->
          <div class="text-center">
            <div class="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mx-auto mb-3">
              <svg class="w-10 h-10 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2c5.523 0 10 4.477 10 10s-4.477 10-10 10-10-4.477-10-10 4.477-10 10-10zm0 18c4.418 0 8-3.582 8-8s-3.582-8-8-8-8 3.582-8 8 3.582 8 8 8z"/>
              </svg>
            </div>
            <h3 class="font-semibold text-gray-900 dark:text-white mb-2">{{ t('about.tech.backend') }}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">Django 4, Django REST Framework, NumPy, APScheduler</p>
          </div>

          <!-- Database -->
          <div class="text-center">
            <div class="w-16 h-16 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center mx-auto mb-3">
              <svg class="w-10 h-10 text-purple-600 dark:text-purple-400" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 3c-1.66 0-3 1.34-3 3v12c0 1.66 1.34 3 3 3s3-1.34 3-3v-12c0-1.66-1.34-3-3-3zm0 16c-.55 0-1-.45-1-1v-12c0-.55.45-1 1-1s1 .45 1 1v12c0 .55-.45 1-1 1z"/>
              </svg>
            </div>
            <h3 class="font-semibold text-gray-900 dark:text-white mb-2">{{ t('about.tech.database') }}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">PostgreSQL, SQLite</p>
          </div>
        </div>
      </div>

      <!-- Links -->
      <div class="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl shadow-xl p-8 text-white">
        <h2 class="text-2xl font-bold mb-6">{{ t('about.links.documentation') }}</h2>
        <div class="grid grid-cols-1 md:grid-cols-3gap-4">
          <a href="https://github.com/yourusername/matrixcalc" target="_blank" class="flex items-center gap-3 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg p-4 transition-colors">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            <span class="font-medium">{{ t('about.links.github') }}</span>
          </a>
          <a href="/docs" class="flex items-center gap-3 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg p-4 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
            </svg>
            <span class="font-medium">{{ t('about.links.documentation') }}</span>
          </a>
          <a href="https://opensource.org/licenses/MIT" target="_blank" class="flex items-center gap-3 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg p-4 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
            <span class="font-medium">{{ t('about.links.license') }}</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
