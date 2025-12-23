<template>
  <div
    class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 transition-colors duration-200"
  >
    <div class="p-6 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ t("calculator.matrixList.title") }}
          </h3>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {{ totalCount }} matrices en total
          </p>
        </div>
        <button
          @click="refreshList"
          :disabled="loading"
          class="px-4 py-2 text-sm font-medium bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 transition-all flex items-center gap-2"
        >
          <svg
            v-if="loading"
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
          {{ loading ? t("common.loading") : "Actualizar" }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading && matrices.length === 0" class="p-12">
      <LoadingSpinner size="lg" message="Cargando matrices..." />
    </div>

    <!-- Empty State -->
    <div v-else-if="matrices.length === 0" class="p-12 text-center">
      <svg
        class="mx-auto h-16 w-16 text-gray-400 dark:text-gray-600"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"
        />
      </svg>
      <p class="mt-4 text-sm font-medium text-gray-900 dark:text-white">
        {{ t("calculator.matrixList.empty") }}
      </p>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
        Crea una nueva matriz para comenzar
      </p>
    </div>

    <!-- Matrix List -->
    <ul v-else class="divide-y divide-gray-200 dark:divide-gray-700">
      <li
        v-for="matrix in sortedMatrices"
        :key="matrix.id"
        class="p-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
      >
        <div class="flex items-center justify-between">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <h4
                class="text-sm font-medium text-gray-900 dark:text-white truncate"
              >
                {{ matrix.name }}
              </h4>
              <span
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200"
              >
                {{ matrix.rows }}×{{ matrix.cols }}
              </span>
            </div>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Creada: {{ formatDate(matrix.created_at) }}
            </p>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-1 ml-4">
            <button
              @click="viewMatrix(matrix)"
              class="p-2 text-gray-400 dark:text-gray-500 hover:text-primary-600 dark:hover:text-primary-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              title="Ver matriz"
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
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                />
              </svg>
            </button>

            <button
              @click="editMatrix(matrix)"
              class="p-2 text-gray-400 dark:text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              title="Editar"
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
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </button>

            <button
              @click="selectForOperation(matrix)"
              class="p-2 text-gray-400 dark:text-gray-500 hover:text-green-600 dark:hover:text-green-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              title="Usar en operación"
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
                  d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                />
              </svg>
            </button>

            <button
              @click="exportCSV(matrix)"
              class="p-2 text-gray-400 dark:text-gray-500 hover:text-indigo-600 dark:hover:text-indigo-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              title="Exportar CSV"
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
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </button>

            <button
              @click="confirmDelete(matrix)"
              class="p-2 text-gray-400 dark:text-gray-500 hover:text-red-600 dark:hover:text-red-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              title="Eliminar"
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
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          </div>
        </div>
      </li>
    </ul>

    <!-- Confirmation Modal -->
    <ConfirmationModal
      v-model="showDeleteModal"
      title="Eliminar Matriz"
      :message="`¿Estás seguro de que quieres eliminar la matriz &quot;${deleteCandidate?.name}&quot;? Esta acción no se puede deshacer.`"
      confirm-text="Eliminar"
      cancel-text="Cancelar"
      type="danger"
      @confirm="deleteMatrix"
      @cancel="cancelDelete"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { storeToRefs } from "pinia";
import { useMatrixStore } from "@/stores/matrixStore";
import { useToast } from "@/composables/useToast";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import ConfirmationModal from "@/components/ConfirmationModal.vue";
import type { Matrix } from "@/types/matrix";

const { t } = useI18n();
const { success, error: showError, info } = useToast();

const emit = defineEmits<{
  view: [matrix: Matrix];
  edit: [matrix: Matrix];
  select: [matrix: Matrix];
}>();

const matrixStore = useMatrixStore();
const { matrices, totalCount, sortedMatrices } = storeToRefs(matrixStore);

const loading = ref(false);
const deleteCandidate = ref<Matrix | null>(null);
const showDeleteModal = ref(false);

onMounted(async () => {
  await refreshList();
});

async function refreshList() {
  loading.value = true;
  try {
    await matrixStore.fetchMatrices();
    info(`✨ ${totalCount.value} matrices cargadas`);
  } catch (err) {
    showError(`Error al cargar matrices: ${err}`);
  } finally {
    loading.value = false;
  }
}

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString("es-ES", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function viewMatrix(matrix: Matrix) {
  emit("view", matrix);
  info(`👁️ Visualizando "${matrix.name}"`);
}

function editMatrix(matrix: Matrix) {
  emit("edit", matrix);
  info(`✏️ Editando "${matrix.name}"`);
}

function selectForOperation(matrix: Matrix) {
  emit("select", matrix);
  success(`✅ Matriz "${matrix.name}" seleccionada para operación`);
}

async function exportCSV(matrix: Matrix) {
  try {
    await matrixStore.exportMatrixCSV(matrix.id, `${matrix.name}.csv`);
    success(`📥 Matriz "${matrix.name}" exportada a CSV`);
  } catch (err) {
    showError(`Error al exportar: ${err}`);
  }
}

function confirmDelete(matrix: Matrix) {
  deleteCandidate.value = matrix;
  showDeleteModal.value = true;
}

function cancelDelete() {
  deleteCandidate.value = null;
  showDeleteModal.value = false;
}

async function deleteMatrix() {
  if (!deleteCandidate.value) return;

  try {
    const matrixName = deleteCandidate.value.name;
    await matrixStore.deleteMatrix(deleteCandidate.value.id);
    success(`🗑️ Matriz "${matrixName}" eliminada correctamente`);
    deleteCandidate.value = null;
  } catch (err) {
    showError(`Error al eliminar: ${err}`);
  }
}
</script>
