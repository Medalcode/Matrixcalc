<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="isOpen"
        class="fixed inset-0 bg-black/50 dark:bg-black/70 z-50 flex items-center justify-center p-4"
        @click.self="close"
      >
        <div
          class="w-full max-w-3xl bg-white dark:bg-gray-800 rounded-2xl shadow-2xl overflow-hidden max-h-[90vh] flex flex-col"
          @click.stop
        >
          <!-- Header -->
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between">
              <div>
                <h2
                  class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2"
                >
                  📄 Exportar a LaTeX
                </h2>
                <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {{ matrix?.name }} ({{ matrix?.rows }}×{{ matrix?.cols }})
                </p>
              </div>
              <button
                @click="close"
                class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-smooth"
                title="Cerrar (Esc)"
              >
                <svg
                  class="w-6 h-6 text-gray-500 dark:text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>

          <!-- Content -->
          <div class="flex-1 overflow-y-auto p-6 space-y-4">
            <!-- Format Selection -->
            <div>
              <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >
                Formato de Exportación
              </label>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-2">
                <button
                  v-for="format in exportFormats"
                  :key="format.value"
                  @click="selectedFormat = format.value"
                  :class="[
                    'px-4 py-2 text-sm rounded-lg border-2 transition-smooth',
                    selectedFormat === format.value
                      ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300'
                      : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600',
                  ]"
                >
                  {{ format.label }}
                </button>
              </div>
            </div>

            <!-- LaTeX Preview -->
            <div>
              <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >
                Preview LaTeX
              </label>
              <div class="relative">
                <pre
                  class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-4 overflow-x-auto text-sm font-mono text-gray-800 dark:text-gray-200"
                  >{{ latexOutput }}</pre
                >
                <button
                  @click="copyLaTeX"
                  class="absolute top-2 right-2 px-3 py-1.5 bg-primary-600 hover:bg-primary-700 text-white text-xs rounded-md transition-smooth flex items-center gap-1"
                  title="Copiar al portapapeles"
                >
                  <svg
                    v-if="!copied"
                    class="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                    />
                  </svg>
                  <svg
                    v-else
                    class="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  {{ copied ? "¡Copiado!" : "Copiar" }}
                </button>
              </div>
            </div>

            <!-- Usage Instructions -->
            <div
              class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4"
            >
              <h4
                class="font-semibold text-blue-900 dark:text-blue-300 mb-2 flex items-center gap-2"
              >
                💡 Cómo usar en LaTeX
              </h4>
              <ul class="text-sm text-blue-800 dark:text-blue-300 space-y-1">
                <li>
                  • Requiere el paquete
                  <code class="bg-blue-100 dark:bg-blue-800 px-1 rounded"
                    >amsmath</code
                  >
                </li>
                <li>
                  • Pega el código dentro de un entorno matemático:
                  <code class="bg-blue-100 dark:bg-blue-800 px-1 rounded"
                    >\[ ... \]</code
                  >
                  o
                  <code class="bg-blue-100 dark:bg-blue-800 px-1 rounded"
                    >$$ ... $$</code
                  >
                </li>
                <li v-if="selectedFormat === 'document'">
                  • Este formato incluye un documento completo listo para
                  compilar
                </li>
              </ul>
            </div>
          </div>

          <!-- Footer -->
          <div
            class="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 flex justify-between items-center"
          >
            <div class="text-sm text-gray-600 dark:text-gray-400">
              {{ latexOutput.length }} caracteres
            </div>
            <div class="flex gap-2">
              <button
                @click="downloadLaTeX"
                class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-smooth"
              >
                📥 Descargar .tex
              </button>
              <button
                @click="close"
                class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-smooth"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import type { Matrix } from "@/types/matrix";
import {
  exportToLaTeX,
  exportToLaTeXEquation,
  copyToClipboard,
  downloadAsFile,
  getAvailableFormats,
  getFormatDescription,
  type LaTeXFormat,
} from "@/utils/exporters/latexExporter";
import { useToast } from "@/composables/useToast";

const props = defineProps<{
  matrix: Matrix | null;
  modelValue: boolean;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: boolean];
}>();

const { success, error } = useToast();

const isOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

const selectedFormat = ref<LaTeXFormat>("bmatrix");
const precision = ref(2);
const includeEquation = ref(false);
const copied = ref(false);

const exportFormats = getAvailableFormats().map((format) => ({
  value: format,
  label: getFormatDescription(format),
}));

const latexOutput = computed(() => {
  if (!props.matrix || !props.matrix.data) return "";

  try {
    if (includeEquation.value) {
      const label = props.matrix.name.replace(/\s+/g, "_").toLowerCase();
      return exportToLaTeXEquation(props.matrix.data, label, {
        format: selectedFormat.value,
        precision: precision.value,
      });
    }

    return exportToLaTeX(props.matrix.data, {
      format: selectedFormat.value,
      precision: precision.value,
    });
  } catch (err) {
    console.error("LaTeX export error:", err);
    return "% Error al generar LaTeX";
  }
});

async function copyLaTeX() {
  const result = await copyToClipboard(latexOutput.value);

  if (result) {
    copied.value = true;
    success("📋 Código LaTeX copiado al portapapeles");

    setTimeout(() => {
      copied.value = false;
    }, 2000);
  } else {
    error("❌ Error al copiar al portapapeles");
  }
}

function downloadLaTeX() {
  if (!props.matrix) return;

  const filename = `${props.matrix.name.replace(/\s+/g, "_")}.tex`;
  downloadAsFile(latexOutput.value, filename);
  success(`📥 Archivo ${filename} descargado`);
}

function close() {
  isOpen.value = false;
  selectedFormat.value = "bmatrix";
  precision.value = 2;
  includeEquation.value = false;
  copied.value = false;
}

// Reset on close
watch(isOpen, (newVal) => {
  if (!newVal) {
    selectedFormat.value = "bmatrix";
    precision.value = 2;
    includeEquation.value = false;
    copied.value = false;
  }
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

code {
  font-family: "Courier New", Courier, monospace;
}
</style>
