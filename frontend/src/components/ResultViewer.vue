<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="mb-4 flex items-center justify-between">
      <div>
        <h3 class="text-lg font-medium text-gray-900">
          {{ t("calculator.result.title") }}
        </h3>
        <p class="text-sm text-gray-500" v-if="matrix">{{ matrix.name }}</p>
      </div>
      <button
        v-if="onClose"
        @click="onClose"
        class="text-gray-400 hover:text-gray-600"
      >
        <svg
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
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

    <div v-if="!matrix" class="text-center py-12 text-gray-500">
      {{ t("calculator.result.noResult") }}
    </div>

    <div v-else>
      <!-- Matrix Info -->
      <div class="mb-4 p-3 bg-gray-50 rounded-md">
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span class="text-gray-500">Dimensiones:</span>
            <span class="ml-2 font-medium"
              >{{ matrix.rows }} × {{ matrix.cols }}</span
            >
          </div>
          <div v-if="operation">
            <span class="text-gray-500"
              >{{ t("calculator.result.executionTime") }}:</span
            >
            <span class="ml-2 font-medium"
              >{{ operation.execution_time_ms }}{{ t("common.ms") }}</span
            >
          </div>
        </div>
      </div>

      <!-- Determinant Special Case -->
      <div
        v-if="
          isDeterminant &&
          determinantValue !== null &&
          determinantValue !== undefined
        "
        class="mb-4"
      >
        <div class="p-4 bg-primary-50 border border-primary-200 rounded-lg">
          <p class="text-sm text-gray-600 mb-1">Determinante:</p>
          <p class="text-3xl font-bold text-primary-900">
            {{ formatNumber(determinantValue!) }}
          </p>
        </div>
      </div>

      <!-- Matrix Display -->
      <div class="overflow-x-auto mb-4">
        <div class="inline-block min-w-full">
          <div
            class="grid gap-1 p-4 bg-gray-50 rounded-lg"
            :style="{
              gridTemplateColumns: `repeat(${matrix.cols}, minmax(80px, 1fr))`,
            }"
          >
            <div
              v-for="(value, index) in flatMatrix"
              :key="index"
              class="px-3 py-2 bg-white border border-gray-200 rounded text-center font-mono text-sm"
            >
              {{ formatNumber(value) }}
            </div>
          </div>
        </div>
      </div>

      <!-- Operation Details -->
      <div v-if="operation" class="mb-4 p-3 border border-gray-200 rounded-md">
        <h4 class="text-sm font-medium text-gray-900 mb-2">
          Detalles de la Operación
        </h4>
        <div class="space-y-1 text-sm text-gray-600">
          <p>
            <span class="font-medium">Tipo:</span>
            {{ getOperationName(operation.operation_type) }}
          </p>
          <p v-if="operation.matrix_a">
            <span class="font-medium">Matriz A:</span>
            {{ operation.matrix_a.name }}
          </p>
          <p v-if="operation.matrix_b">
            <span class="font-medium">Matriz B:</span>
            {{ operation.matrix_b.name }}
          </p>
          <p>
            <span class="font-medium">Fecha:</span>
            {{ formatDate(operation.created_at) }}
          </p>
        </div>
      </div>

      <!-- Advanced Results -->
      <div v-if="operation?.extra_data" class="mb-4 space-y-4">
        <!-- Rank Special Display -->
        <div
          v-if="operation.operation_type === 'RANK'"
          class="p-4 bg-purple-50 border border-purple-200 rounded-lg"
        >
          <p class="text-sm text-gray-600 mb-1">Rango calculado:</p>
          <p class="text-3xl font-bold text-purple-900">
            {{ operation.extra_data.rank }}
          </p>
        </div>

        <!-- Eigenvalues Special Display -->
        <div
          v-if="
            operation.operation_type === 'EIGEN' &&
            operation.extra_data.eigenvalues
          "
          class="bg-indigo-50 border border-indigo-200 rounded-lg p-4"
        >
          <h4 class="font-bold text-indigo-900 mb-2">
            Valores Propios (Eigenvalues)
          </h4>
          <div class="grid gap-1">
            <div
              v-for="(ev, idx) in operation.extra_data.eigenvalues"
              :key="idx"
              class="font-mono text-sm bg-white/50 px-2 py-1 rounded"
            >
              λ{{ idx + 1 }} = {{ formatComplex(ev) }}
            </div>
          </div>
        </div>

        <!-- Generic Matrix Viewer for Extra Data Matrices -->
        <div v-for="(val, key) in operation.extra_data" :key="key">
          <template
            v-if="
              ['U', 'Vh', 'Q', 'R', 'L', 'eigenvectors'].includes(
                String(key),
              ) && Array.isArray(val)
            "
          >
            <div class="mt-4 border border-gray-200 rounded-lg overflow-hidden">
              <div
                class="bg-gray-100 px-3 py-2 text-xs font-bold uppercase tracking-wider border-b border-gray-200 text-gray-600"
              >
                Matriz {{ key }}
                <span class="font-normal text-gray-400 ml-2" v-if="val.length"
                  >({{ val.length }}×{{ val[0]?.length }})</span
                >
              </div>
              <div
                class="overflow-x-auto p-2 bg-gray-50 max-h-60 overflow-y-auto theme-scroll"
              >
                <div
                  class="inline-block"
                  :style="{
                    display: 'grid',
                    gridTemplateColumns: `repeat(${val[0]?.length || 1}, minmax(60px, 1fr))`,
                    gap: '2px',
                  }"
                >
                  <template v-for="(row, rIdx) in val" :key="rIdx">
                    <div
                      v-for="(cell, cIdx) in row"
                      :key="`${rIdx}-${cIdx}`"
                      class="px-2 py-1 bg-white border border-gray-100 rounded text-xs text-center font-mono whitespace-nowrap truncate hover:overflow-visible hover:relative hover:z-10 hover:shadow-md"
                    >
                      {{
                        typeof cell === "object"
                          ? formatComplex(cell)
                          : formatNumber(Number(cell))
                      }}
                    </div>
                  </template>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex gap-2">
        <button
          @click="copyToClipboard"
          class="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200"
        >
          Copiar Datos
        </button>
        <button
          @click="exportCSV"
          class="flex-1 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Exportar CSV
        </button>
      </div>

      <!-- Copy Success Message -->
      <div
        v-if="copySuccess"
        class="mt-2 p-2 bg-green-50 border border-green-200 rounded text-sm text-green-800 text-center"
      >
        ¡Datos copiados al portapapeles!
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";
import { useMatrixStore } from "@/stores/matrixStore";
import type { Matrix, Operation, OperationType } from "@/types/matrix";

const { t } = useI18n();

const props = defineProps<{
  matrix?: Matrix;
  operation?: Operation;
  onClose?: () => void;
}>();

const matrixStore = useMatrixStore();
const copySuccess = ref(false);

const flatMatrix = computed(() => {
  if (!props.matrix) return [];
  return props.matrix.data.flat();
});

const isDeterminant = computed(
  () => props.operation?.operation_type === "DETERMINANT",
);

const determinantValue = computed(() => {
  if (!isDeterminant.value || !props.matrix || !props.matrix.data[0])
    return null;
  // El determinante se guarda como matriz 1x1
  return props.matrix.data[0][0];
});

function formatNumber(value: number): string {
  if (Math.abs(value) < 0.0001 && value !== 0) {
    return value.toExponential(4);
  }
  return value.toFixed(4).replace(/\.?0+$/, "");
}

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleString("es-ES", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatComplex(val: any): string {
  if (typeof val === "string") return val;
  if (typeof val === "number") return formatNumber(val);
  if (val && typeof val === "object" && "real" in val) {
    const r = val.real;
    const i = val.imag;
    if (Math.abs(i) < 1e-10) return formatNumber(r);
    const sign = i >= 0 ? "+" : "-";
    return `${formatNumber(r)} ${sign} ${formatNumber(Math.abs(i))}i`;
  }
  return String(val);
}

function getOperationName(type: OperationType): string {
  const names: Record<OperationType, string> = {
    SUM: "Suma",
    SUBTRACT: "Resta",
    MULTIPLY: "Multiplicación",
    INVERSE: "Inversa",
    DETERMINANT: "Determinante",
    TRANSPOSE: "Transpuesta",
    RANK: "Rango",
    EIGEN: "Eigenvalores/Vectores",
    SVD: "Descomposición SVD",
    QR: "Descomposición QR",
    CHOLESKY: "Descomposición Cholesky",
  };
  return names[type] || type;
}

async function copyToClipboard() {
  if (!props.matrix) return;

  const text = props.matrix.data.map((row) => row.join("\t")).join("\n");

  try {
    await navigator.clipboard.writeText(text);
    copySuccess.value = true;
    setTimeout(() => {
      copySuccess.value = false;
    }, 2000);
  } catch (err) {
    console.error("Error copying to clipboard:", err);
  }
}

async function exportCSV() {
  if (!props.matrix) return;

  try {
    await matrixStore.exportMatrixCSV(
      props.matrix.id,
      `${props.matrix.name}.csv`,
    );
  } catch (err) {
    console.error("Error exporting CSV:", err);
  }
}
</script>
