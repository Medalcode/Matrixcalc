<template>
  <div class="matrix-heatmap bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        🎨 Visualización Heatmap
      </h3>
      <div class="flex items-center gap-2">
        <select
          v-model="selectedColorScale"
          class="px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="viridis">Viridis</option>
          <option value="plasma">Plasma</option>
          <option value="cool">Cool</option>
          <option value="warm">Warm</option>
          <option value="rainbow">Rainbow</option>
        </select>
      </div>
    </div>

    <!-- Heatmap Grid -->
    <div class="overflow-x-auto">
      <div 
        class="inline-grid gap-1 p-2 bg-gray-50 dark:bg-gray-900 rounded-lg"
        :style="{ gridTemplateColumns: `repeat(${matrix.cols}, minmax(50px, 1fr))` }"
      >
        <div
          v-for="(value, index) in flatMatrix"
          :key="index"
          :style="{ backgroundColor: getCellColor(value) }"
          :title="`Value: ${formatNumber(value)}\nRow: ${getRow(index) + 1}, Col: ${getCol(index) + 1}`"
          class="relative group aspect-square flex items-center justify-center rounded border border-gray-300 dark:border-gray-600 cursor-help transition-transform hover:scale-110 hover:z-10"
        >
          <!-- Value (optional, can be toggled) -->
          <span 
            v-if="showValues"
            :class="[
              'text-xs font-semibold',
              getTextColor(value)
            ]"
          >
            {{ formatNumber(value) }}
          </span>

          <!-- Tooltip on hover -->
          <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-20">
            <div>Valor: {{ formatNumber(value) }}</div>
            <div class="text-gray-300 dark:text-gray-600">Pos: [{{ getRow(index) + 1 }}, {{ getCol(index) + 1 }}]</div>
            <div 
              class="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-gray-900 dark:border-t-gray-100"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Legend -->
    <div class="mt-4 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="text-sm text-gray-600 dark:text-gray-400">Min:</span>
        <span class="text-sm font-semibold text-gray-900 dark:text-white">{{ formatNumber(minValue) }}</span>
      </div>
      <div class="flex-1 mx-4 h-6 rounded-full" :style="{ background: gradientCSS }"></div>
      <div class="flex items-center gap-2">
        <span class="text-sm text-gray-600 dark:text-gray-400">Max:</span>
        <span class="text-sm font-semibold text-gray-900 dark:text-white">{{ formatNumber(maxValue) }}</span>
      </div>
    </div>

    <!-- Options -->
    <div class="mt-4 flex items-center gap-4">
      <label class="flex items-center gap-2 cursor-pointer">
        <input
          v-model="showValues"
          type="checkbox"
          class="rounded border-gray-300 dark:border-gray-600 text-primary-600 focus:ring-primary-500"
        />
        <span class="text-sm text-gray-700 dark:text-gray-300">Mostrar valores</span>
      </label>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { Matrix } from '@/types/matrix';

const props = defineProps<{
  matrix: Matrix;
}>();

const selectedColorScale = ref<'viridis' | 'plasma' | 'cool' | 'warm' | 'rainbow'>('viridis');
const showValues = ref(true);

const flatMatrix = computed(() => props.matrix.data.flat());
const minValue = computed(() => Math.min(...flatMatrix.value));
const maxValue = computed(() => Math.max(...flatMatrix.value));

// Color scales
const colorScales = {
  viridis: ['#440154', '#31688e', '#35b779', '#fde724'],
  plasma: ['#0d0887', '#7e03a8', '#cc4778', '#f89540', '#f0f921'],
  cool: ['#00ffff', '#0080ff', '#0000ff', '#8000ff'],
  warm: ['#ffff00', '#ff8000', '#ff0000', '#800000'],
  rainbow: ['#ff0000', '#ff8000', '#ffff00', '#00ff00', '#0080ff', '#0000ff', '#8000ff']
};

function getCellColor(value: number): string {
  const range = maxValue.value - minValue.value;
  if (range === 0) return colorScales[selectedColorScale.value][0];
  
  const normalized = (value - minValue.value) / range;
  return interpolateColor(normalized, colorScales[selectedColorScale.value]);
}

function interpolateColor(t: number, colors: string[]): string {
  const segments = colors.length - 1;
  const segment = Math.floor(t * segments);
  const localT = (t * segments) - segment;
  
  const color1 = colors[Math.min(segment, segments)];
  const color2 = colors[Math.min(segment + 1, segments)];
  
  return blendColors(color1, color2, localT);
}

function blendColors(color1: string, color2: string, t: number): string {
  const c1 = hexToRgb(color1);
  const c2 = hexToRgb(color2);
  
  const r = Math.round(c1.r + (c2.r - c1.r) * t);
  const g = Math.round(c1.g + (c2.g - c1.g) * t);
  const b = Math.round(c1.b + (c2.b - c1.b) * t);
  
  return `rgb(${r}, ${g}, ${b})`;
}

function hexToRgb(hex: string): { r: number; g: number; b: number } {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : { r: 0, g: 0, b: 0 };
}

function getTextColor(value: number): string {
  const range = maxValue.value - minValue.value;
  if (range === 0) return 'text-white';
  
  const normalized = (value - minValue.value) / range;
  return normalized > 0.5 ? 'text-white' : 'text-gray-900 dark:text-white';
}

function getRow(index: number): number {
  return Math.floor(index / props.matrix.cols);
}

function getCol(index: number): number {
  return index % props.matrix.cols;
}

function formatNumber(num: number): string {
  if (Number.isInteger(num)) return num.toString();
  return num.toFixed(2);
}

const gradientCSS = computed(() => {
  const colors = colorScales[selectedColorScale.value];
  return `linear-gradient(to right, ${colors.join(', ')})`;
});
</script>

<style scoped>
.matrix-heatmap {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
