<template>
  <div
    class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200"
  >
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        {{ t("calculator.operations.title") }}
      </h3>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        Selecciona matrices y ejecuta operaciones
      </p>
    </div>

    <!-- Selected Matrices -->
    <div class="space-y-4 mb-6">
      <div>
        <label
          class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >{{ t("calculator.operations.selectMatrixA") }}</label
        >
        <div class="flex items-center gap-2">
          <select
            v-model="selectedMatrixAId"
            class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
          >
            <option :value="null">
              {{ t("calculator.operations.selectMatrix") }}...
            </option>
            <option
              v-for="matrix in availableMatrices"
              :key="matrix.id"
              :value="matrix.id"
            >
              {{ matrix.name }} ({{ matrix.rows }}×{{ matrix.cols }})
            </option>
          </select>
          <button
            v-if="selectedMatrixA"
            @click="viewMatrix(selectedMatrixA)"
            class="p-2 text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 border border-gray-300 dark:border-gray-600 rounded-md transition-colors"
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
        </div>
      </div>

      <div v-if="requiresTwoMatrices">
        <label
          class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >{{ t("calculator.operations.selectMatrixB") }}</label
        >
        <div class="flex items-center gap-2">
          <select
            v-model="selectedMatrixBId"
            class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
          >
            <option :value="null">
              {{ t("calculator.operations.selectMatrix") }}...
            </option>
            <option
              v-for="matrix in availableMatrices"
              :key="matrix.id"
              :value="matrix.id"
            >
              {{ matrix.name }} ({{ matrix.rows }}×{{ matrix.cols }})
            </option>
          </select>
          <button
            v-if="selectedMatrixB"
            @click="viewMatrix(selectedMatrixB)"
            class="p-2 text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 border border-gray-300 dark:border-gray-600 rounded-md transition-colors"
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
        </div>
      </div>
    </div>

    <!-- Operations -->
    <div class="mb-6">
      <label
        class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3"
        >Operaciones</label
      >

      <!-- Binary Operations -->
      <div class="mb-4">
        <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">
          Operaciones con dos matrices
        </p>
        <div class="grid grid-cols-3 gap-2">
          <button
            @click="selectOperation('sum')"
            :disabled="!canPerformBinaryOperation"
            :class="[
              'p-3 rounded-lg border-2 transition-all',
              selectedOperation === 'sum'
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900 text-primary-700 dark:text-primary-300'
                : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-500 text-gray-700 dark:text-gray-300',
              !canPerformBinaryOperation && 'opacity-50 cursor-not-allowed',
            ]"
          >
            <div class="text-2xl mb-1">+</div>
            <div class="text-xs">
              {{ t("calculator.operations.types.sum") }}
            </div>
          </button>

          <button
            @click="selectOperation('subtract')"
            :disabled="!canPerformBinaryOperation"
            :class="[
              'p-3 rounded-lg border-2 transition-all',
              selectedOperation === 'subtract'
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900 text-primary-700 dark:text-primary-300'
                : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-500 text-gray-700 dark:text-gray-300',
              !canPerformBinaryOperation && 'opacity-50 cursor-not-allowed',
            ]"
          >
            <div class="text-2xl mb-1">−</div>
            <div class="text-xs">
              {{ t("calculator.operations.types.subtract") }}
            </div>
          </button>

          <button
            @click="selectOperation('multiply')"
            :disabled="!canPerformBinaryOperation"
            :class="[
              'p-3 rounded-lg border-2 transition-all',
              selectedOperation === 'multiply'
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900 text-primary-700 dark:text-primary-300'
                : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-500 text-gray-700 dark:text-gray-300',
              !canPerformBinaryOperation && 'opacity-50 cursor-not-allowed',
            ]"
          >
            <div class="text-2xl mb-1">×</div>
            <div class="text-xs">
              {{ t("calculator.operations.types.multiply") }}
            </div>
          </button>
        </div>
      </div>

      <!-- Unary Operations -->
      <div>
        <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">
          Operaciones con una matriz
        </p>
        <div class="grid grid-cols-3 gap-2">
          <button
            @click="selectOperation('inverse')"
            :disabled="!canPerformUnaryOperation"
            :class="[
              'p-3 rounded-lg border-2 transition-all',
              selectedOperation === 'inverse'
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900 text-primary-700 dark:text-primary-300'
                : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-500 text-gray-700 dark:text-gray-300',
              !canPerformUnaryOperation && 'opacity-50 cursor-not-allowed',
            ]"
          >
            <div class="text-2xl mb-1">A⁻¹</div>
            <div class="text-xs">
              {{ t("calculator.operations.types.inverse") }}
            </div>
          </button>

          <button
            @click="selectOperation('determinant')"
            :disabled="!canPerformUnaryOperation"
            :class="[
              'p-3 rounded-lg border-2 transition-all',
              selectedOperation === 'determinant'
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900 text-primary-700 dark:text-primary-300'
                : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-500 text-gray-700 dark:text-gray-300',
              !canPerformUnaryOperation && 'opacity-50 cursor-not-allowed',
            ]"
          >
            <div class="text-2xl mb-1">|A|</div>
            <div class="text-xs">Determinante</div>
          </button>

          <button
            @click="selectOperation('transpose')"
            :disabled="!canPerformUnaryOperation"
            :class="[
              'p-3 rounded-lg border-2 transition-all',
              selectedOperation === 'transpose'
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900 text-primary-700 dark:text-primary-300'
                : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-500 text-gray-700 dark:text-gray-300',
              !canPerformUnaryOperation && 'opacity-50 cursor-not-allowed',
            ]"
          >
            <div class="text-2xl mb-1">Aᵀ</div>
            <div class="text-xs">
              {{ t("calculator.operations.types.transpose") }}
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="mb-4 p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
      <LoadingSpinner size="md" message="Calculando operación..." />
    </div>

    <!-- Validation Messages -->
    <div
      v-if="validationMessage && !loading"
      class="mb-4 p-3 bg-yellow-50 dark:bg-yellow-900 border border-yellow-200 dark:border-yellow-700 rounded-md"
    >
      <p class="text-sm text-yellow-800 dark:text-yellow-200">
        ⚠️ {{ validationMessage }}
      </p>
    </div>

    <!-- Execute Button -->
    <button
      @click="executeOperation"
      :disabled="!canExecute || loading"
      class="w-full px-4 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-all flex items-center justify-center gap-2"
    >
      <svg
        v-if="loading"
        class="animate-spin h-5 w-5"
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
      {{ loading ? "Calculando..." : t("calculator.operations.calculate") }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useI18n } from "vue-i18n";
import { storeToRefs } from "pinia";
import { useMatrixStore } from "@/stores/matrixStore";
import { useStatsStore } from "@/stores/statsStore";
import { useToast } from "@/composables/useToast";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import type { Matrix, Operation } from "@/types/matrix";

const { t } = useI18n();
const { success, error: showError, warning, info } = useToast();

const emit = defineEmits<{
  result: [operation: Operation];
  viewMatrix: [matrix: Matrix];
}>();

const matrixStore = useMatrixStore();
const statsStore = useStatsStore();
const { matrices } = storeToRefs(matrixStore);

const selectedMatrixAId = ref<number | null>(null);
const selectedMatrixBId = ref<number | null>(null);
const selectedOperation = ref<
  | "sum"
  | "subtract"
  | "multiply"
  | "inverse"
  | "determinant"
  | "transpose"
  | null
>(null);
const loading = ref(false);

const availableMatrices = computed(() => matrices.value);

const selectedMatrixA = computed(
  () => matrices.value.find((m) => m.id === selectedMatrixAId.value) || null
);

const selectedMatrixB = computed(
  () => matrices.value.find((m) => m.id === selectedMatrixBId.value) || null
);

const requiresTwoMatrices = computed(
  () =>
    selectedOperation.value &&
    ["sum", "subtract", "multiply"].includes(selectedOperation.value)
);

const canPerformUnaryOperation = computed(() => !!selectedMatrixA.value);

const canPerformBinaryOperation = computed(
  () => !!selectedMatrixA.value && !!selectedMatrixB.value
);

const validationMessage = computed(() => {
  if (!selectedOperation.value) return null;

  if (requiresTwoMatrices.value) {
    if (!selectedMatrixA.value || !selectedMatrixB.value) {
      return "Selecciona dos matrices para esta operación";
    }

    if (
      selectedOperation.value === "sum" ||
      selectedOperation.value === "subtract"
    ) {
      if (
        selectedMatrixA.value.rows !== selectedMatrixB.value.rows ||
        selectedMatrixA.value.cols !== selectedMatrixB.value.cols
      ) {
        return "Las matrices deben tener las mismas dimensiones";
      }
    }

    if (selectedOperation.value === "multiply") {
      if (selectedMatrixA.value.cols !== selectedMatrixB.value.rows) {
        return `El número de columnas de A (${selectedMatrixA.value.cols}) debe ser igual al número de filas de B (${selectedMatrixB.value.rows})`;
      }
    }
  } else {
    if (!selectedMatrixA.value) {
      return "Selecciona una matriz para esta operación";
    }

    if (
      selectedOperation.value === "inverse" ||
      selectedOperation.value === "determinant"
    ) {
      if (selectedMatrixA.value.rows !== selectedMatrixA.value.cols) {
        return "La matriz debe ser cuadrada para esta operación";
      }
    }
  }

  return null;
});

const canExecute = computed(
  () => !!selectedOperation.value && !validationMessage.value
);

const operationNames: Record<string, string> = {
  sum: "Suma",
  subtract: "Resta",
  multiply: "Multiplicación",
  inverse: "Inversa",
  determinant: "Determinante",
  transpose: "Transpuesta",
};

function selectOperation(operation: typeof selectedOperation.value) {
  selectedOperation.value = operation;
  const opName = operationNames[operation!] || operation;
  info(`Operación seleccionada: ${opName}`);
}

async function executeOperation() {
  if (!canExecute.value || !selectedOperation.value) {
    warning("Verifica que los datos sean correctos antes de ejecutar");
    return;
  }

  loading.value = true;

  try {
    const operation = await statsStore.performOperation(
      selectedOperation.value,
      selectedMatrixAId.value!,
      selectedMatrixBId.value || undefined
    );

    const opName =
      operationNames[selectedOperation.value] || selectedOperation.value;
    success(`✅ ${opName} completada en ${operation.execution_time_ms}ms`);
    emit("result", operation);

    // Refresh matrices list
    await matrixStore.fetchMatrices();
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : String(err);
    showError(`❌ Error en la operación: ${errorMsg}`);
  } finally {
    loading.value = false;
  }
}

function viewMatrix(matrix: Matrix) {
  emit("viewMatrix", matrix);
  info(`👁️ Visualizando "${matrix.name}"`);
}

// Watch for matrix store selections
watch(
  () => matrixStore.selectedMatrixA,
  (newVal) => {
    if (newVal) {
      selectedMatrixAId.value = newVal.id;
      info(`Matriz A seleccionada: "${newVal.name}"`);
    }
  }
);

watch(
  () => matrixStore.selectedMatrixB,
  (newVal) => {
    if (newVal) {
      selectedMatrixBId.value = newVal.id;
      info(`Matriz B seleccionada: "${newVal.name}"`);
    }
  }
);
</script>
