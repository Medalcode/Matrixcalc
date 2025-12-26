/**
 * 📤 useDragDrop - Composable for drag and drop file upload
 * MatrixCalc v3.0
 */

import { ref, onMounted, onUnmounted } from 'vue';

export interface DropZoneOptions {
  accept?: string[]; // File extensions: ['.csv', '.txt', '.json']
  maxSize?: number; // Max file size in bytes
  multiple?: boolean; // Allow multiple files
  onDrop?: (files: File[]) => void;
  onError?: (error: string) => void;
}

export function useDragDrop(elementRef: Ref<HTMLElement | null>, options: DropZoneOptions = {}) {
  const {
    accept = ['.csv', '.txt', '.json'],
    maxSize = 5 * 1024 * 1024, // 5MB default
    multiple = false,
    onDrop,
    onError
  } = options;

  const isDragging = ref(false);
  const dragCounter = ref(0);

  function handleDragEnter(e: DragEvent) {
    e.preventDefault();
    e.stopPropagation();
    
    dragCounter.value++;
    if (dragCounter.value === 1) {
      isDragging.value = true;
    }
  }

  function handleDragLeave(e: DragEvent) {
    e.preventDefault();
    e.stopPropagation();
    
    dragCounter.value--;
    if (dragCounter.value === 0) {
      isDragging.value = false;
    }
  }

  function handleDragOver(e: DragEvent) {
    e.preventDefault();
    e.stopPropagation();
  }

  function handleDrop(e: DragEvent) {
    e.preventDefault();
    e.stopPropagation();
    
    isDragging.value = false;
    dragCounter.value = 0;

    const files = Array.from(e.dataTransfer?.files || []);
    
    if (files.length === 0) {
      onError?.('No se detectaron archivos');
      return;
    }

    // Validate file count
    if (!multiple && files.length > 1) {
      onError?.('Solo se permite un archivo a la vez');
      return;
    }

    // Validate file types
    const validFiles = files.filter(file => {
      const ext = '.' + file.name.split('.').pop()?.toLowerCase();
      return accept.includes(ext);
    });

    if (validFiles.length === 0) {
      onError?.(`Solo se permiten archivos: ${accept.join(', ')}`);
      return;
    }

    // Validate file sizes
    const oversizedFiles = validFiles.filter(file => file.size > maxSize);
    if (oversizedFiles.length > 0) {
      const maxMB = (maxSize / (1024 * 1024)).toFixed(1);
      onError?.(`Los archivos deben ser menores a ${maxMB}MB`);
      return;
    }

    // All validations passed
    onDrop?.(validFiles);
  }

  function setupListeners() {
    const element = elementRef.value;
    if (!element) return;

    element.addEventListener('dragenter', handleDragEnter);
    element.addEventListener('dragleave', handleDragLeave);
    element.addEventListener('dragover', handleDragOver);
    element.addEventListener('drop', handleDrop);
  }

  function removeListeners() {
    const element = elementRef.value;
    if (!element) return;

    element.removeEventListener('dragenter', handleDragEnter);
    element.removeEventListener('dragleave', handleDragLeave);
    element.removeEventListener('dragover', handleDragOver);
    element.removeEventListener('drop', handleDrop);
  }

  onMounted(() => {
    setupListeners();
  });

  onUnmounted(() => {
    removeListeners();
  });

  return {
    isDragging,
    setupListeners,
    removeListeners
  };
}

/**
 * Parse CSV file to matrix data
 */
export async function parseCSVFile(file: File): Promise<number[][]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        const text = e.target?.result as string;
        const lines = text.trim().split('\n');
        
        const matrix = lines.map(line => {
          const values = line.split(',').map(v => {
            const num = parseFloat(v.trim());
            if (isNaN(num)) throw new Error(`Valor inválido: ${v}`);
            return num;
          });
          return values;
        });

        // Validate all rows have same length
        const cols = matrix[0].length;
        const allSameLength = matrix.every(row => row.length === cols);
        
        if (!allSameLength) {
          throw new Error('Todas las filas deben tener el mismo número de columnas');
        }

        resolve(matrix);
      } catch (error) {
        reject(error);
      }
    };

    reader.onerror = () => reject(new Error('Error al leer el archivo'));
    reader.readAsText(file);
  });
}

/**
 * Parse JSON file to matrix data
 */
export async function parseJSONFile(file: File): Promise<number[][]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        const text = e.target?.result as string;
        const json = JSON.parse(text);
        
        // Support different JSON formats
        let matrix: number[][];
        
        if (Array.isArray(json.data)) {
          matrix = json.data;
        } else if (Array.isArray(json)) {
          matrix = json;
        } else {
          throw new Error('Formato JSON no soportado');
        }

        // Validate matrix structure
        if (!Array.isArray(matrix[0])) {
          throw new Error('El JSON debe contener una matriz 2D');
        }

        const cols = matrix[0].length;
        const allSameLength = matrix.every(row => row.length === cols);
        
        if (!allSameLength) {
          throw new Error('Todas las filas deben tener el mismo número de columnas');
        }

        resolve(matrix);
      } catch (error) {
        reject(error);
      }
    };

    reader.onerror = () => reject(new Error('Error al leer el archivo'));
    reader.readAsText(file);
  });
}
