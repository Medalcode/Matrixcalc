<template>
  <div class="py-12 bg-gray-50 dark:bg-gray-900 min-h-screen transition-colors duration-200">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          📚 Documentación
        </h1>
        <p class="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
          Guía completa para usar MatrixCalc - Calculadora de Matrices
        </p>
      </div>

      <!-- Quick Start -->
      <div class="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl shadow-xl p-8 mb-8 text-white">
        <h2 class="text-2xl font-bold mb-4 flex items-center gap-2">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Inicio Rápido
        </h2>
        <div class="space-y-3">
          <p>1. Crea una nueva matriz en la pestaña <strong>"Calculadora"</strong></p>
          <p>2. Usa las <strong>plantillas predefinidas</strong> para llenar rápidamente</p>
          <p>3. Ejecuta operaciones desde el <strong>Panel de Operaciones</strong></p>
          <p>4. Visualiza resultados y <strong>estadísticas</strong></p>
        </div>
      </div>

      <!-- Features Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <!-- Calculator -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-gray-700 transition-colors duration-200">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
              <svg class="w-7 h-7 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white">Calculadora</h3>
          </div>
          <ul class="space-y-2 text-gray-600 dark:text-gray-300">
            <li class="flex items-start gap-2">
              <span class="text-green-500 dark:text-green-400 mt-1">✓</span>
              <span>Crea matrices de cualquier tamaño (hasta 100×100)</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-green-500 dark:text-green-400 mt-1">✓</span>
              <span>14 plantillas predefinidas disponibles</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-green-500 dark:text-green-400 mt-1">✓</span>
              <span>Edita valores directamente en la cuadrícula</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-green-500 dark:text-green-400 mt-1">✓</span>
              <span>Botones rápidos: Zeros, Ones, Identity, Random</span>
            </li>
          </ul>
        </div>

        <!-- Operations -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-gray-700 transition-colors duration-200">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
              <svg class="w-7 h-7 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white">Operaciones</h3>
          </div>
          <ul class="space-y-2 text-gray-600 dark:text-gray-300">
            <li class="flex items-start gap-2">
              <span class="text-blue-500 dark:text-blue-400 mt-1">+</span>
              <span><strong>Suma:</strong> A + B (mismas dimensiones)</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-blue-500 dark:text-blue-400 mt-1">−</span>
              <span><strong>Resta:</strong> A − B (mismas dimensiones)</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-blue-500 dark:text-blue-400 mt-1">×</span>
              <span><strong>Multiplicación:</strong> A × B (cols A = rows B)</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-blue-500 dark:text-blue-400 mt-1">⁻¹</span>
              <span><strong>Inversa:</strong> A⁻¹ (matriz cuadrada)</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-blue-500 dark:text-blue-400 mt-1">|A|</span>
              <span><strong>Determinante:</strong> det(A) (matriz cuadrada)</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-blue-500 dark:text-blue-400 mt-1">ᵀ</span>
              <span><strong>Transpuesta:</strong> Aᵀ</span>
            </li>
          </ul>
        </div>

        <!-- Import/Export -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-gray-700 transition-colors duration-200">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
              <svg class="w-7 h-7 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white">Import/Export</h3>
          </div>
          <ul class="space-y-2 text-gray-600 dark:text-gray-300">
            <li class="flex items-start gap-2">
              <span class="text-purple-500 dark:text-purple-400 mt-1">📥</span>
              <span><strong>Importar CSV:</strong> Carga matrices desde archivo CSV</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-purple-500 dark:text-purple-400 mt-1">📤</span>
              <span><strong>Exportar CSV:</strong> Descarga matrices individuales</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-purple-500 dark:text-purple-400 mt-1">💾</span>
              <span><strong>Backup JSON:</strong> Exporta todas tus matrices</span>
            </li>
          </ul>
        </div>

        <!-- Stats -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-gray-700 transition-colors duration-200">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 bg-yellow-100 dark:bg-yellow-900 rounded-lg flex items-center justify-center">
              <svg class="w-7 h-7 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white">Estadísticas</h3>
          </div>
          <ul class="space-y-2 text-gray-600 dark:text-gray-300">
            <li class="flex items-start gap-2">
              <span class="text-yellow-500 dark:text-yellow-400 mt-1">📊</span>
              <span>Visualiza total de matrices y operaciones</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-yellow-500 dark:text-yellow-400 mt-1">📈</span>
              <span>Gráficos interactivos con Chart.js</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-yellow-500 dark:text-yellow-400 mt-1">⏱️</span>
              <span>Tiempos de ejecución de operaciones</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- Templates -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8 border border-gray-200 dark:border-gray-700 transition-colors duration-200">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
          <span>📐</span> Plantillas Disponibles
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div class="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Básicas</h4>
            <ul class="text-sm space-y-1 text-gray-600 dark:text-gray-400">
              <li>• Zeros</li>
              <li>• Ones</li>
              <li>• Random (0-1)</li>
              <li>• Random (-10 to 10)</li>
            </ul>
          </div>
          <div class="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Especiales</h4>
            <ul class="text-sm space-y-1 text-gray-600 dark:text-gray-400">
              <li>• Identity</li>
              <li>• Diagonal</li>
              <li>• Upper Triangular</li>
              <li>• Lower Triangular</li>
            </ul>
          </div>
          <div class="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Transformación</h4>
            <ul class="text-sm space-y-1 text-gray-600 dark:text-gray-400">
              <li>• Rotation 2D</li>
              <li>• Scaling 2D</li>
            </ul>
          </div>
          <div class="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Ejemplos</h4>
            <ul class="text-sm space-y-1 text-gray-600 dark:text-gray-400">
              <li>• Checkerboard</li>
              <li>• Hilbert Matrix</li>
              <li>• Vandermonde</li>
              <li>• Pascal Triangle</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Keyboard Shortcuts -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8 border border-gray-200 dark:border-gray-700 transition-colors duration-200">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
          <span>⌨️</span> Atajos de Teclado (Próximamente)
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="flex justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded">
            <span class="text-gray-700 dark:text-gray-300">Guardar matriz</span>
            <kbd class="px-2 py-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded text-xs">Ctrl+S</kbd>
          </div>
          <div class="flex justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded">
            <span class="text-gray-700 dark:text-gray-300">Cerrar modal</span>
            <kbd class="px-2 py-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded text-xs">Esc</kbd>
          </div>
        </div>
      </div>

      <!-- Dark Mode -->
      <div class="bg-gradient-to-r from-gray-800 to-gray-900 rounded-2xl shadow-xl p-8 text-white">
        <h2 class="text-2xl font-bold mb-4 flex items-center gap-2">
          <span>🌙</span> Dark Mode
        </h2>
        <p class="mb-4">MatrixCalc incluye soporte completo para modo oscuro con 3 opciones:</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white bg-opacity-10 p-4 rounded-lg">
            <div class="text-2xl mb-2">☀️</div>
            <h4 class="font-semibold mb-1">Light</h4>
            <p class="text-sm opacity-90">Modo claro siempre activo</p>
          </div>
          <div class="bg-white bg-opacity-10 p-4 rounded-lg">
            <div class="text-2xl mb-2">🌙</div>
            <h4 class="font-semibold mb-1">Dark</h4>
            <p class="text-sm opacity-90">Modo oscuro siempre activo</p>
          </div>
          <div class="bg-white bg-opacity-10 p-4 rounded-lg">
            <div class="text-2xl mb-2">⚙️</div>
            <h4 class="font-semibold mb-1">Auto</h4>
            <p class="text-sm opacity-90">Sigue preferencia del sistema</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// No logic needed for this documentation page
</script>
