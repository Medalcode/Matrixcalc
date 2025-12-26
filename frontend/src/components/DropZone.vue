<template>
  <div
    ref="dropZoneRef"
    :class="[
      'relative border-2 border-dashed rounded-lg p-8 transition-all duration-200',
      isDragging
        ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
        : 'border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800/50 hover:border-gray-400 dark:hover:border-gray-500'
    ]"
  >
    <!-- Drop Zone Content -->
    <div class="text-center">
      <!-- Icon -->
      <div class="mb-4">
        <svg 
          :class="[
            'mx-auto h-12 w-12 transition-colors',
            isDragging 
              ? 'text-primary-500' 
              : 'text-gray-400 dark:text-gray-500'
          ]"
          stroke="currentColor" 
          fill="none" 
          viewBox="0 0 48 48"
        >
          <path 
            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
          />
        </svg>
      </div>

      <!-- Text -->
      <div class="space-y-2">
        <p :class="[
          'text-lg font-semibold',
          isDragging 
            ? 'text-primary-700 dark:text-primary-300' 
            : 'text-gray-700 dark:text-gray-300'
        ]">
          {{ isDragging ? '¡Suelta el archivo aquí!' : 'Arrastra y suelta un archivo' }}
        </p>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          o 
          <button
            @click="openFilePicker"
            class="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium underline"
          >
            haz clic para seleccionar
          </button>
        </p>
      </div>

      <!-- Accepted formats -->
      <div class="mt-4">
        <p class="text-xs text-gray-500 dark:text-gray-400">
          Formatos soportados: {{ acceptedFormats.join(', ') }}
        </p>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
          Tamaño máximo: {{ maxSizeMB }}MB
        </p>
      </div>
    </div>

    <!-- Hidden file input -->
    <input
      ref="fileInputRef"
      type="file"
      :accept="accept.join(',')"
      :multiple="multiple"
      class="hidden"
      @change="handleFileSelect"
    />

    <!-- Loading overlay -->
    <div
      v-if="isLoading"
      class="absolute inset-0 bg-white/90 dark:bg-gray-800/90 rounded-lg flex items-center justify-center"
    >
      <div class="text-center">
        <svg class="animate-spin h-10 w-10 text-primary-600 mx-auto mb-2" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-sm text-gray-600 dark:text-gray-400">Procesando archivo...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useDragDrop, parseCSVFile, parseJSONFile } from '@/composables/useDragDrop';
import { useToast } from '@/composables/useToast';

const props = withDefaults(defineProps<{
  accept?: string[];
  maxSize?: number;
  multiple?: boolean;
}>(), {
  accept: () => ['.csv', '.txt', '.json'],
  maxSize: 5 * 1024 * 1024, // 5MB
  multiple: false
});

const emit = defineEmits<{
  'file-dropped': [data: number[][], filename: string];
}>();

const { success, error: showError } = useToast();

const dropZoneRef = ref<HTMLElement | null>(null);
const fileInputRef = ref<HTMLInputElement | null>(null);
const isLoading = ref(false);

const maxSizeMB = computed(() => (props.maxSize / (1024 * 1024)).toFixed(1));
const acceptedFormats = computed(() => props.accept.map(ext => ext.toUpperCase()));

const { isDragging } = useDragDrop(dropZoneRef, {
  accept: props.accept,
  maxSize: props.maxSize,
  multiple: props.multiple,
  onDrop: handleFileDrop,
  onError: (error) => showError(error)
});

async function handleFileDrop(files: File[]) {
  const file = files[0];
  await processFile(file);
}

function openFilePicker() {
  fileInputRef.value?.click();
}

async function handleFileSelect(event: Event) {
  const input = event.target as HTMLInputElement;
  const files = Array.from(input.files || []);
  
  if (files.length > 0) {
    await processFile(files[0]);
  }
  
  // Reset input
  input.value = '';
}

async function processFile(file: File) {
  isLoading.value = true;
  
  try {
    let matrixData: number[][];
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (ext === '.csv' || ext === '.txt') {
      matrixData = await parseCSVFile(file);
    } else if (ext === '.json') {
      matrixData = await parseJSONFile(file);
    } else {
      throw new Error('Formato de archivo no soportado');
    }
    
    emit('file-dropped', matrixData, file.name);
    success(`✅ Archivo "${file.name}" cargado exitosamente`);
  } catch (err) {
    showError(`Error al procesar archivo: ${err instanceof Error ? err.message : String(err)}`);
  } finally {
    isLoading.value = false;
  }
}
</script>
