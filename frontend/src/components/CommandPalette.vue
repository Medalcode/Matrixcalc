<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="isOpen"
        class="fixed inset-0 bg-black/50 dark:bg-black/70 z-50 flex items-start justify-center pt-32 px-4"
        @click.self="close"
      >
        <div 
          class="w-full max-w-2xl bg-white dark:bg-gray-800 rounded-xl shadow-2xl overflow-hidden transition-smooth"
          @click.stop
        >
          <!-- Search Input -->
          <div class="p-4 border-b border-gray-200 dark:border-gray-700">
            <div class="relative">
              <svg 
                class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              
              <input
                ref="searchInput"
                v-model="searchQuery"
                type="text"
                placeholder="Buscar comandos..."
                class="w-full pl-10 pr-4 py-3 bg-gray-50 dark:bg-gray-700 border-0 rounded-lg
                       text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400
                       focus:outline-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400"
                @keydown.down.prevent="selectNext"
                @keydown.up.prevent="selectPrevious"
                @keydown.enter.prevent="executeSelected"
                @keydown.esc="close"
              />
              
              <kbd class="absolute right-3 top-1/2 -translate-y-1/2 px-2 py-1 text-xs font-semibold
                        text-gray-500 dark:text-gray-400 bg-gray-200 dark:bg-gray-600 rounded">
                Esc
              </kbd>
            </div>
          </div>

          <!-- Commands List -->
          <div class="max-h-96 overflow-y-auto">
            <div v-if="filteredCommands.length === 0" class="p-8 text-center">
              <p class="text-gray-500 dark:text-gray-400">
                No se encontraron comandos para "{{ searchQuery }}"
              </p>
            </div>

            <div v-else>
              <!-- Group by category -->
              <div v-for="(commands, category) in groupedCommands" :key="category" class="py-2">
                <div class="px-4 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                  {{ getCategoryName(category) }}
                </div>

                <button
                  v-for="(command, index) in commands"
                  :key="command.id"
                  class="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-100 dark:hover:bg-gray-700
                         transition-smooth cursor-pointer group"
                  :class="{
                    'bg-primary-50 dark:bg-primary-900/30': selectedIndex === getGlobalIndex(category, index)
                  }"
                  @click="execute(command)"
                  @mouseenter="selectedIndex = getGlobalIndex(category, index)"
                >
                  <div class="flex items-center gap-3 flex-1">
                    <span class="text-2xl">{{ command.icon }}</span>
                    <div class="text-left">
                      <div class="text-sm font-medium text-gray-900 dark:text-white">
                        {{ command.name }}
                      </div>
                      <div class="text-xs text-gray-500 dark:text-gray-400">
                        {{ command.description }}
                      </div>
                    </div>
                  </div>

                  <kbd 
                    v-if="command.shortcut"
                    class="px-2 py-1 text-xs font-semibold text-gray-600 dark:text-gray-300
                           bg-gray-200 dark:bg-gray-600 rounded"
                  >
                    {{ command.shortcut }}
                  </kbd>
                </button>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="p-3 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
            <div class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
              <div class="flex items-center gap-4">
                <span class="flex items-center gap-1">
                  <kbd class="px-1.5 py-0.5 bg-gray-200 dark:bg-gray-600 rounded">↑</kbd>
                  <kbd class="px-1.5 py-0.5 bg-gray-200 dark:bg-gray-600 rounded">↓</kbd>
                  Navegar
                </span>
                <span class="flex items-center gap-1">
                  <kbd class="px-1.5 py-0.5 bg-gray-200 dark:bg-gray-600 rounded">Enter</kbd>
                  Ejecutar
                </span>
              </div>
              <span>{{ filteredCommands.length }} comandos</span>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useMatrixStore } from '@/stores/matrixStore';
import { useToast } from '@/composables/useToast';
import { useTheme } from '@/composables/useTheme';

interface Command {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: 'navigation' | 'matrix' | 'theme' | 'help' | 'export';
  shortcut?: string;
  action: () => void;
}

const router = useRouter();
const matrixStore = useMatrixStore();
const { success, info } = useToast();
const { toggleTheme } = useTheme();

const isOpen = ref(false);
const searchQuery = ref('');
const selectedIndex = ref(0);
const searchInput = ref<HTMLInputElement | null>(null);

// Define all available commands
const allCommands = computed<Command[]>(() => [
  // Navigation
  {
    id: 'nav-home',
    name: 'Ir a Inicio',
    description: 'Página principal de MatrixCalc',
    icon: '🏠',
    category: 'navigation',
    shortcut: 'Alt+H',
    action: () => router.push('/')
  },
  {
    id: 'nav-calculator',
    name: 'Ir a Calculadora',
    description: 'Crear y editar matrices',
    icon: '📐',
    category: 'navigation',
    shortcut: 'Alt+1',
    action: () => router.push('/calculator')
  },
  {
    id: 'nav-stats',
    name: 'Ir a Estadísticas',
    description: 'Ver estadísticas de uso',
    icon: '📊',
    category: 'navigation',
    shortcut: 'Alt+2',
    action: () => router.push('/stats')
  },
  {
    id: 'nav-docs',
    name: 'Ir a Documentación',
    description: 'Guías y tutoriales',
    icon: '📚',
    category: 'navigation',
    shortcut: 'Alt+3',
    action: () => router.push('/docs')
  },
  {
    id: 'nav-about',
    name: 'Acerca de',
    description: 'Información del proyecto',
    icon: 'ℹ️',
    category: 'navigation',
    shortcut: 'Alt+4',
    action: () => router.push('/about')
  },

  // Matrix Operations
  {
    id: 'matrix-new',
    name: 'Nueva Matriz',
    description: 'Crear una nueva matriz',
    icon: '➕',
    category: 'matrix',
    shortcut: 'Ctrl+N',
    action: () => {
      matrixStore.clearSelections();
      router.push('/calculator');
      success('Nueva matriz creada');
    }
  },
  {
    id: 'matrix-list',
    name: 'Listar Matrices',
    description: 'Ver todas las matrices guardadas',
    icon: '📋',
    category: 'matrix',
    shortcut: 'Ctrl+L',
    action: () => {
      router.push('/calculator');
      info('Lista de matrices');
    }
  },
  {
    id: 'matrix-identity',
    name: 'Crear Matriz Identidad',
    description: 'Generar matriz identidad 3x3',
    icon: '🔢',
    category: 'matrix',
    action: () => {
      router.push('/calculator');
      info('Aplica la plantilla Identidad desde el editor');
    }
  },
  {
    id: 'matrix-random',
    name: 'Crear Matriz Aleatoria',
    description: 'Generar matriz con valores aleatorios',
    icon: '🎲',
    category: 'matrix',
    action: () => {
      router.push('/calculator');
      info('Aplica la plantilla Random desde el editor');
    }
  },

  // Theme
  {
    id: 'theme-toggle',
    name: 'Cambiar Tema',
    description: 'Alternar entre modo claro y oscuro',
    icon: '🌓',
    category: 'theme',
    shortcut: 'Ctrl+D',
    action: () => toggleTheme()
  },

  // Help
  {
    id: 'help-shortcuts',
    name: 'Atajos de Teclado',
    description: 'Ver todos los atajos disponibles',
    icon: '⌨️',
    category: 'help',
    shortcut: 'Ctrl+/',
    action: () => {
      dispatchEvent(new CustomEvent('show-shortcuts-help'));
      close();
    }
  },

  // Export
  {
    id: 'export-csv',
    name: 'Exportar a CSV',
    description: 'Exportar matriz seleccionada a CSV',
    icon: '📥',
    category: 'export',
    action: () => {
      info('Selecciona una matriz y usa el botón de exportar');
    }
  }
]);

// Filter commands based on search query
const filteredCommands = computed(() => {
  if (!searchQuery.value.trim()) {
    return allCommands.value;
  }

  const query = searchQuery.value.toLowerCase();
  return allCommands.value.filter(cmd =>
    cmd.name.toLowerCase().includes(query) ||
    cmd.description.toLowerCase().includes(query) ||
    cmd.category.toLowerCase().includes(query)
  );
});

// Group commands by category
const groupedCommands = computed(() => {
  const grouped: Record<string, Command[]> = {};
  
  filteredCommands.value.forEach(cmd => {
    if (!grouped[cmd.category]) {
      grouped[cmd.category] = [];
    }
    grouped[cmd.category]?.push(cmd);
  });

  return grouped;
});

const getCategoryName = (category: string): string => {
  const names: Record<string, string> = {
    navigation: 'Navegación',
    matrix: 'Matrices',
    theme: 'Apariencia',
    help: 'Ayuda',
    export: 'Exportar'
  };
  return names[category] || category;
};

const getGlobalIndex = (category: string, localIndex: number): number => {
  let globalIndex = 0;
  const categories = Object.keys(groupedCommands.value);
  
  for (const cat of categories) {
    if (cat === category) {
      return globalIndex + localIndex;
    }
    globalIndex += (groupedCommands.value[cat]?.length || 0);
  }
  
  return globalIndex;
};

const selectNext = () => {
  if (selectedIndex.value < filteredCommands.value.length - 1) {
    selectedIndex.value++;
  }
};

const selectPrevious = () => {
  if (selectedIndex.value > 0) {
    selectedIndex.value--;
  }
};

const executeSelected = () => {
  const command = filteredCommands.value[selectedIndex.value];
  if (command) {
    execute(command);
  }
};

const execute = (command: Command) => {
  command.action();
  close();
};

const open = () => {
  isOpen.value = true;
  searchQuery.value = '';
  selectedIndex.value = 0;
  
  nextTick(() => {
    searchInput.value?.focus();
  });
};

const close = () => {
  isOpen.value = false;
  searchQuery.value = '';
};

const handleToggle = () => {
  if (isOpen.value) {
    close();
  } else {
    open();
  }
};

// Watch for search query changes to reset selection
watch(searchQuery, () => {
  selectedIndex.value = 0;
});

// Listen for custom event to toggle palette
onMounted(() => {
  window.addEventListener('toggle-command-palette', handleToggle);
});

onUnmounted(() => {
  window.removeEventListener('toggle-command-palette', handleToggle);
});

defineExpose({
  open,
  close,
  isOpen
});
</script>

<style scoped>
/* Ensure smooth keyboard navigation scrolling */
button:focus {
  outline: none;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
