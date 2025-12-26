<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="isOpen"
        class="fixed inset-0 bg-black/50 dark:bg-black/70 z-50 flex items-center justify-center p-4"
        @click.self="close"
      >
        <div 
          class="w-full max-w-4xl bg-white dark:bg-gray-800 rounded-2xl shadow-2xl overflow-hidden max-h-[90vh] flex flex-col"
          @click.stop
        >
          <!-- Header -->
          <div class="p-6 border-b border-gray-200 dark:border-gray-700 bg-linear-to-r from-primary-50 to-purple-50 dark:from-gray-900 dark:to-gray-800">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                  ⌨️ Atajos de Teclado
                </h2>
                <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Usa estos atajos para navegar más rápido
                </p>
              </div>
              <button
                @click="close"
                class="p-2 hover:bg-white/50 dark:hover:bg-gray-700 rounded-lg transition-smooth"
                title="Cerrar (Esc)"
              >
                <svg class="w-6 h-6 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Content -->
          <div class="flex-1 overflow-y-auto p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Category: Navigation -->
              <div class="space-y-3">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                  🧭 Navegación
                </h3>
                <div class="space-y-2">
                  <ShortcutRow 
                    v-for="shortcut in navigationShortcuts"
                    :key="shortcut.key"
                    :shortcut="formatShortcut(shortcut)"
                    :description="shortcut.description"
                  />
                </div>
              </div>

              <!-- Category: Matrix Operations -->
              <div class="space-y-3">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                  🔢 Operaciones de Matrices
                </h3>
                <div class="space-y-2">
                  <ShortcutRow 
                    v-for="shortcut in matrixShortcuts"
                    :key="shortcut.key"
                    :shortcut="formatShortcut(shortcut)"
                    :description="shortcut.description"
                  />
                </div>
              </div>

              <!-- Category: General -->
              <div class="space-y-3">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                  ⚙️ General
                </h3>
                <div class="space-y-2">
                  <ShortcutRow 
                    v-for="shortcut in generalShortcuts"
                    :key="shortcut.key"
                    :shortcut="formatShortcut(shortcut)"
                    :description="shortcut.description"
                  />
                </div>
              </div>

              <!-- Category: Editing -->
              <div class="space-y-3">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                  ✏️ Edición
                </h3>
                <div class="space-y-2">
                  <ShortcutRow 
                    v-for="shortcut in editingShortcuts"
                    :key="shortcut.key"
                    :shortcut="formatShortcut(shortcut)"
                    :description="shortcut.description"
                  />
                  <ShortcutRow 
                    shortcut="Tab / Shift+Tab"
                    description="Navegar entre celdas de matriz"
                  />
                  <ShortcutRow 
                    shortcut="Enter"
                    description="Ejecutar operación"
                  />
                  <ShortcutRow 
                    shortcut="Esc"
                    description="Cerrar modal/diálogo"
                  />
                </div>
              </div>
            </div>

            <!-- Pro Tips -->
            <div class="mt-8 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
              <h4 class="font-semibold text-blue-900 dark:text-blue-300 flex items-center gap-2 mb-2">
                💡 Consejos Pro
              </h4>
              <ul class="space-y-1 text-sm text-blue-800 dark:text-blue-300">
                <li>• Presiona <kbd class="kbd">Ctrl+K</kbd> para abrir el Command Palette y buscar cualquier acción</li>
                <li>• Usa <kbd class="kbd">Alt + 1-4</kbd> para cambiar rápidamente entre secciones</li>
                <li>• Presiona <kbd class="kbd">Ctrl+D</kbd> para cambiar entre modo claro y oscuro</li>
                <li>• <kbd class="kbd">Ctrl+S</kbd> guarda la matriz actual automáticamente</li>
              </ul>
            </div>
          </div>

          <!-- Footer -->
          <div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 text-center">
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Presiona <kbd class="kbd">Esc</kbd> o haz clic fuera para cerrar
            </p>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useKeyboardShortcuts } from '@/composables/useKeyboardShortcuts';

const { getShortcutsByCategory, formatShortcut } = useKeyboardShortcuts();

const isOpen = ref(false);

const navigationShortcuts = computed(() => getShortcutsByCategory('navigation'));
const matrixShortcuts = computed(() => getShortcutsByCategory('matrix'));
const generalShortcuts = computed(() => getShortcutsByCategory('general'));
const editingShortcuts = computed(() => getShortcutsByCategory('editing'));

const open = () => {
  isOpen.value = true;
};

const close = () => {
  isOpen.value = false;
};

const handleEscape = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && isOpen.value) {
    close();
  }
};

const handleShowShortcuts = () => {
  open();
};

onMounted(() => {
  document.addEventListener('keydown', handleEscape);
  window.addEventListener('show-shortcuts-help', handleShowShortcuts);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape);
  window.removeEventListener('show-shortcuts-help', handleShowShortcuts);
});

defineExpose({
  open,
  close
});
</script>

<script lang="ts">
// Shortcut Row Component
import { defineComponent, h } from 'vue';

const ShortcutRow = defineComponent({
  name: 'ShortcutRow',
  props: {
    shortcut: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    }
  },
  setup(props) {
    return () => h(
      'div',
      { class: 'flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-smooth' },
      [
        h('span', { class: 'text-sm text-gray-700 dark:text-gray-300' }, props.description),
        h('kbd', { class: 'kbd' }, props.shortcut)
      ]
    );
  }
});

export { ShortcutRow };
</script>

<style scoped>
.kbd {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  line-height: 1rem;
  font-weight: 600;
  color: rgb(55 65 81);
  background-color: white;
  border: 1px solid rgb(209 213 219);
  border-radius: 0.25rem;
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
}

.dark .kbd {
  color: rgb(209 213 219);
  background-color: rgb(75 85 99);
  border-color: rgb(107 114 128);
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
