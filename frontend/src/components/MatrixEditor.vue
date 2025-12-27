<template>
  <div
    class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200"
  >
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        {{ t("calculator.editor.title") }}
      </h3>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        Crea o edita una matriz
      </p>
    </div>

    <!-- Matrix Name and Dimensions -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
      <div>
        <label
          class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >{{ t("calculator.editor.name") }}</label
        >
        <input
          v-model="matrixName"
          type="text"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
          :placeholder="t('calculator.editor.namePlaceholder')"
        />
      </div>
      <div>
        <label
          class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >{{ t("calculator.editor.rows") }}</label
        >
        <input
          v-model.number="rows"
          type="number"
          min="1"
          max="100"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
          @change="resizeMatrix"
        />
      </div>
      <div>
        <label
          class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >{{ t("calculator.editor.cols") }}</label
        >
        <input
          v-model.number="cols"
          type="number"
          min="1"
          max="100"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
          @change="resizeMatrix"
        />
      </div>
    </div>

    <!-- Templates Dropdown -->
    <div class="mb-4">
      <label
        class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
      >
        <span class="flex items-center gap-2">
          📐 Plantillas Predefinidas
          <span class="text-xs text-gray-500 dark:text-gray-400 font-normal"
            >(opcional)</span
          >
        </span>
      </label>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
        <button
          v-for="template in filteredTemplates"
          :key="template.name"
          @click="applyTemplate(template)"
          class="px-3 py-2 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors text-left"
          :title="template.description"
        >
          {{ template.name }}
        </button>
      </div>
    </div>

    <!-- Matrix Grid -->
    <div
      id="matrix-grid"
      class="mb-4 overflow-x-auto bg-gray-50 dark:bg-gray-900 rounded-lg p-4 transition-colors"
    >
      <LoadingSpinner v-if="loading" size="lg" message="Guardando matriz..." />
      <div v-else class="inline-block min-w-full">
        <div
          class="grid gap-1"
          :style="{ gridTemplateColumns: `repeat(${cols}, minmax(60px, 1fr))` }"
        >
          <input
            v-for="(value, index) in flatMatrix"
            :key="index"
            v-model.number="flatMatrix[index]"
            type="number"
            step="any"
            class="px-2 py-1.5 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded text-center focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
            @input="updateMatrix"
          />
        </div>
      </div>
    </div>

    <!-- Quick Fill Actions -->
    <div class="flex flex-wrap gap-2 mb-4">
      <button
        @click="fillZeros"
        class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
      >
        {{ t("calculator.editor.actions.fillZeros") }}
      </button>
      <button
        @click="fillOnes"
        class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
      >
        {{ t("calculator.editor.actions.fillOnes") }}
      </button>
      <button
        @click="fillIdentity"
        :disabled="rows !== cols"
        class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {{ t("calculator.editor.actions.fillIdentity") }}
      </button>
      <button
        @click="fillRandom"
        class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
      >
        {{ t("calculator.editor.actions.fillRandom") }}
      </button>
    </div>

    <!-- Actions -->
    <div class="flex gap-2 mt-4">
      <button
        @click="saveMatrix"
        :disabled="loading || !isValidMatrix"
        class="flex-1 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2 shadow-md"
      >
        <span v-if="loading">
          <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
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
        </span>
        💾 {{
          loading
            ? t("common.loading")
            : editMode
            ? "Actualizar"
            : "Guardar Matriz"
        }}
      </button>
      <button
        v-if="editMode"
        @click="cancelEdit"
        :disabled="loading"
        class="px-6 py-3 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-semibold rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 transition-colors"
      >
        {{ t("calculator.editor.actions.cancel") }}
      </button>
      <button
        v-else
        @click="clearMatrix"
        :disabled="loading"
        class="px-6 py-3 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-semibold rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 transition-colors"
      >
        Limpiar
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useMatrixStore } from "@/stores/matrixStore";
import { useToast } from "@/composables/useToast";
import { useAnimations } from "@/composables/useAnimations";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import { matrixTemplates, type MatrixTemplate } from "@/utils/matrixTemplates";
import type { Matrix } from "@/types/matrix";

const { t } = useI18n();
const { success, error: showError, info } = useToast();
const { matrixFlip, confetti, shake } = useAnimations();

const props = defineProps<{
  matrix?: Matrix;
}>();

const emit = defineEmits<{
  saved: [matrix: Matrix];
  cancelled: [];
}>();

const matrixStore = useMatrixStore();

const matrixName = ref(props.matrix?.name || "");
const rows = ref(props.matrix?.rows || 3);
const cols = ref(props.matrix?.cols || 3);
const flatMatrix = ref<number[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const successMessage = ref<string | null>(null);

const editMode = computed(() => !!props.matrix);

const isValidMatrix = computed(() => {
  return (
    matrixName.value.trim().length > 0 &&
    rows.value > 0 &&
    cols.value > 0 &&
    flatMatrix.value.length === rows.value * cols.value &&
    flatMatrix.value.every((v) => !isNaN(v))
  );
});

// Initialize matrix
function initializeMatrix() {
  if (props.matrix) {
    flatMatrix.value = props.matrix.data.flat();
  } else {
    flatMatrix.value = Array(rows.value * cols.value).fill(0);
  }
}

// Resize matrix when dimensions change
function resizeMatrix() {
  const newSize = rows.value * cols.value;
  const currentSize = flatMatrix.value.length;

  if (newSize > currentSize) {
    // Add zeros for new cells
    flatMatrix.value = [
      ...flatMatrix.value,
      ...Array(newSize - currentSize).fill(0),
    ];
  } else if (newSize < currentSize) {
    // Truncate
    flatMatrix.value = flatMatrix.value.slice(0, newSize);
  }
}

function updateMatrix() {
  // Ensure all values are numbers
  flatMatrix.value = flatMatrix.value.map((v) => (isNaN(v) ? 0 : v));
}

// Quick fill functions
function fillZeros() {
  flatMatrix.value = Array(rows.value * cols.value).fill(0);
}

function fillOnes() {
  flatMatrix.value = Array(rows.value * cols.value).fill(1);
}

function fillIdentity() {
  if (rows.value !== cols.value) return;

  flatMatrix.value = Array(rows.value * cols.value)
    .fill(0)
    .map((_, index) => {
      const row = Math.floor(index / cols.value);
      const col = index % cols.value;
      return row === col ? 1 : 0;
    });
}

function fillRandom() {
  flatMatrix.value = Array(rows.value * cols.value)
    .fill(0)
    .map(() => Math.floor(Math.random() * 11));
}

// Templates functionality
const filteredTemplates = computed(() => {
  // Show only 8 most useful templates
  const priorityTemplates = ['Zeros', 'Ones', 'Identity', 'Random (0-1)', 'Random (-10 to 10)', 'Diagonal', 'Upper Triangular', 'Lower Triangular'];
  return matrixTemplates.filter(t => priorityTemplates.includes(t.name));
});

function applyTemplate(template: MatrixTemplate) {
  // Animate the matrix grid with flip effect
  matrixFlip('matrix-grid', () => {
    // Generate the matrix data (2D array)
    const matrix2D = template.generateData(rows.value, cols.value);
    
    // Flatten to 1D array for editor
    flatMatrix.value = matrix2D.flat();
    
    // Show success toast
    info(`📐 Plantilla "${template.name}" aplicada`);
  });
}

function clearMatrix() {
  matrixName.value = "";
  rows.value = 3;
  cols.value = 3;
  fillZeros();
  error.value = null;
  successMessage.value = null;
}

// Convert flat array to 2D array
function get2DMatrix(): number[][] {
  const matrix: number[][] = [];
  for (let i = 0; i < rows.value; i++) {
    matrix.push(flatMatrix.value.slice(i * cols.value, (i + 1) * cols.value));
  }
  return matrix;
}

async function saveMatrix() {
  if (!isValidMatrix.value) return;

  loading.value = true;
  error.value = null;
  successMessage.value = null;

  try {
    const matrixData = {
      name: matrixName.value.trim(),
      rows: rows.value,
      cols: cols.value,
      data: get2DMatrix(),
    };

    if (editMode.value && props.matrix) {
      const updated = await matrixStore.updateMatrix(
        props.matrix.id,
        matrixData
      );
      successMessage.value = "Matriz actualizada exitosamente";
      emit("saved", updated);
    } else {
      const newMatrix = await matrixStore.createMatrix(matrixData);
      successMessage.value = "Matriz guardada exitosamente";
      success("✅ Matriz guardada exitosamente");
      confetti(50); // Celebrate with confetti!
      emit("saved", newMatrix);
      clearMatrix();
    }

    setTimeout(() => {
      successMessage.value = null;
    }, 3000);
  } catch (err) {
    error.value = String(err);
    shake('matrix-grid'); // Shake on error
    showError("Error al guardar: " + String(err));
  } finally {
    loading.value = false;
  }
}

function cancelEdit() {
  emit("cancelled");
}

// Watch for prop changes
watch(
  () => props.matrix,
  () => {
    if (props.matrix) {
      matrixName.value = props.matrix.name;
      rows.value = props.matrix.rows;
      cols.value = props.matrix.cols;
      flatMatrix.value = props.matrix.data.flat();
    }
  },
  { immediate: true }
);

// Initialize on mount
initializeMatrix();
</script>
