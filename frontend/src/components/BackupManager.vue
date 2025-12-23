<template>
  <div
    class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200"
  >
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        {{ t("calculator.backup.title") }}
      </h3>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        Importa y exporta tus matrices
      </p>
    </div>

    <!-- Export Section -->
    <div
      class="mb-6 p-4 border border-gray-200 dark:border-gray-700 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800 rounded-lg transition-colors"
    >
      <div class="flex items-start gap-3">
        <div class="flex-shrink-0">
          <svg
            class="h-8 w-8 text-blue-600 dark:text-blue-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"
            />
          </svg>
        </div>
        <div class="flex-1">
          <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">
            {{ t("calculator.backup.export.title") }}
          </h4>
          <p class="text-sm text-gray-600 dark:text-gray-300 mb-4">
            Descarga todas tus matrices en formato JSON con metadatos
          </p>
          <button
            @click="exportBackup"
            :disabled="exporting"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 transition-all flex items-center gap-2"
          >
            <svg
              v-if="exporting"
              class="animate-spin h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            {{
              exporting ? "Exportando..." : t("calculator.backup.export.all")
            }}
          </button>
        </div>
      </div>
    </div>

    <!-- Import Section -->
    <div
      class="mb-6 p-4 border border-gray-200 dark:border-gray-700 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-gray-900 dark:to-gray-800 rounded-lg transition-colors"
    >
      <div class="flex items-start gap-3">
        <div class="flex-shrink-0">
          <svg
            class="h-8 w-8 text-green-600 dark:text-green-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        </div>
        <div class="flex-1">
          <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">
            {{ t("calculator.backup.import.csv") }}
          </h4>
          <p class="text-sm text-gray-600 dark:text-gray-300 mb-4">
            Carga una matriz desde un archivo CSV
          </p>

          <div class="space-y-3">
            <div>
              <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Nombre de la matriz
              </label>
              <input
                v-model="importName"
                type="text"
                placeholder="Ej: Matriz Importada"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors"
              />
            </div>

            <div>
              <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Archivo CSV
              </label>
              <input
                ref="fileInput"
                type="file"
                accept=".csv"
                @change="handleFileSelect"
                class="w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-green-100 dark:file:bg-green-900 file:text-green-700 dark:file:text-green-300 hover:file:bg-green-200 dark:hover:file:bg-green-800 file:transition-colors file:cursor-pointer"
              />
              <p
                v-if="selectedFile"
                class="mt-2 text-xs text-gray-600 dark:text-gray-400"
              >
                📄 Archivo seleccionado: {{ selectedFile.name }}
              </p>
            </div>

            <button
              @click="importCSV"
              :disabled="!selectedFile || !importName.trim() || importing"
              class="w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
            >
              <svg
                v-if="importing"
                class="animate-spin h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              {{ importing ? "Importando..." : "Importar Matriz" }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- CSV Format Help -->
    <div
      class="p-4 bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg transition-colors"
    >
      <h4
        class="text-sm font-semibold text-blue-900 dark:text-blue-200 mb-2 flex items-center gap-2"
      >
        <svg
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        Formato CSV
      </h4>
      <p class="text-xs text-blue-800 dark:text-blue-300 mb-2">
        El archivo CSV debe tener el siguiente formato:
      </p>
      <div
        class="bg-white dark:bg-gray-800 p-3 rounded border border-blue-200 dark:border-blue-600 font-mono text-xs text-gray-900 dark:text-gray-300"
      >
        1,2,3<br />
        4,5,6<br />
        7,8,9
      </div>
      <p class="text-xs text-blue-700 dark:text-blue-300 mt-2">
        ℹ️ Cada línea representa una fila, los valores separados por comas.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { useMatrixStore } from "@/stores/matrixStore";
import { useToast } from "@/composables/useToast";
import type { Matrix } from "@/types/matrix";

const { t } = useI18n();
const { success, error: showError, info } = useToast();

const emit = defineEmits<{
  imported: [matrix: Matrix];
}>();

const matrixStore = useMatrixStore();

const exporting = ref(false);
const importing = ref(false);
const importName = ref("");
const selectedFile = ref<File | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);

function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0 && target.files[0]) {
    selectedFile.value = target.files[0];

    // Auto-fill name from filename if empty
    if (!importName.value.trim()) {
      importName.value = target.files[0].name.replace(".csv", "");
    }

    info(`📄 Archivo seleccionado: ${target.files[0].name}`);
  }
}

async function exportBackup() {
  exporting.value = true;

  try {
    // Fetch all matrices
    await matrixStore.fetchMatrices();
    const matrices = matrixStore.matrices;

    if (matrices.length === 0) {
      showError("No hay matrices para exportar");
      return;
    }

    info(`🔄 Exportando ${matrices.length} matrices...`);

    // Create backup data
    const backupData = {
      version: "2.0",
      timestamp: new Date().toISOString(),
      total_matrices: matrices.length,
      matrices: matrices,
    };

    // Create blob and download
    const blob = new Blob([JSON.stringify(backupData, null, 2)], {
      type: "application/json",
    });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `matrixcalc_backup_${
      new Date().toISOString().split("T")[0]
    }.json`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

    success(`✅ Backup de ${matrices.length} matrices exportado exitosamente`);
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : String(err);
    showError(`❌ Error al exportar backup: ${errorMsg}`);
  } finally {
    exporting.value = false;
  }
}

async function importCSV() {
  if (!selectedFile.value || !importName.value.trim()) {
    showError("Completa el nombre y selecciona un archivo");
    return;
  }

  importing.value = true;

  try {
    info(`🔄 Importando "${importName.value}"...`);

    const matrix = await matrixStore.importMatrixCSV(
      selectedFile.value,
      importName.value.trim()
    );

    success(
      `✅ Matriz "${matrix.name}" importada exitosamente (${matrix.rows}×${matrix.cols})`
    );
    emit("imported", matrix);

    // Reset form
    importName.value = "";
    selectedFile.value = null;
    if (fileInput.value) {
      fileInput.value.value = "";
    }
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : String(err);
    showError(`❌ Error al importar CSV: ${errorMsg}`);
  } finally {
    importing.value = false;
  }
}
</script>
