/**
 * ⌨️ useKeyboardShortcuts - Global keyboard shortcuts
 * MatrixCalc v3.0
 */

import { onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useMatrixStore } from '@/stores/matrixStore';
import { useToast } from './useToast';
import { useTheme } from './useTheme';

export interface KeyboardShortcut {
  key: string;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
  meta?: boolean;
  description: string;
  action: () => void;
  category: 'navigation' | 'matrix' | 'general' | 'editing';
}

export function useKeyboardShortcuts() {
  const router = useRouter();
  const matrixStore = useMatrixStore();
  const { info, success } = useToast();
  const { toggleTheme } = useTheme();

  const shortcuts: KeyboardShortcut[] = [
    // Navigation
    {
      key: '1',
      alt: true,
      description: 'Ir a Calculadora',
      category: 'navigation',
      action: () => {
        router.push('/calculator');
        info('📐 Calculadora');
      }
    },
    {
      key: '2',
      alt: true,
      description: 'Ir a Estadísticas',
      category: 'navigation',
      action: () => {
        router.push('/stats');
        info('📊 Estadísticas');
      }
    },
    {
      key: '3',
      alt: true,
      description: 'Ir a Documentación',
      category: 'navigation',
      action: () => {
        router.push('/docs');
        info('📚 Documentación');
      }
    },
    {
      key: '4',
      alt: true,
      description: 'Ir a Acerca de',
      category: 'navigation',
      action: () => {
        router.push('/about');
        info('ℹ️ Acerca de');
      }
    },
    {
      key: 'h',
      alt: true,
      description: 'Ir a Inicio',
      category: 'navigation',
      action: () => {
        router.push('/');
        info('🏠 Inicio');
      }
    },

    // Matrix Operations
    {
      key: 's',
      ctrl: true,
      description: 'Guardar matriz actual',
      category: 'matrix',
      action: () => {
        // This will be triggered from MatrixEditor
        success('💾 Atajo detectado: Guardar matriz');
      }
    },
    {
      key: 'n',
      ctrl: true,
      description: 'Nueva matriz',
      category: 'matrix',
      action: () => {
        matrixStore.clearSelections();
        router.push('/calculator');
        info('➕ Nueva matriz');
      }
    },
    {
      key: 'l',
      ctrl: true,
      description: 'Listar matrices',
      category: 'matrix',
      action: () => {
        router.push('/calculator');
        info('📋 Lista de matrices');
      }
    },

    // General
    {
      key: 'd',
      ctrl: true,
      description: 'Toggle Dark Mode',
      category: 'general',
      action: () => {
        toggleTheme();
      }
    },
    {
      key: '/',
      ctrl: true,
      description: 'Mostrar ayuda de atajos',
      category: 'general',
      action: () => {
        // Will trigger shortcuts modal
        dispatchEvent(new CustomEvent('show-shortcuts-help'));
      }
    },
    {
      key: 'k',
      ctrl: true,
      description: 'Abrir Command Palette',
      category: 'general',
      action: () => {
        dispatchEvent(new CustomEvent('toggle-command-palette'));
      }
    },

    // Editing
    {
      key: 'z',
      ctrl: true,
      description: 'Deshacer',
      category: 'editing',
      action: () => {
        info('↩️ Deshacer (próximamente)');
      }
    },
    {
      key: 'z',
      ctrl: true,
      shift: true,
      description: 'Rehacer',
      category: 'editing',
      action: () => {
        info('↪️ Rehacer (próximamente)');
      }
    },
  ];

  const handleKeyDown = (event: KeyboardEvent) => {
    // Don't trigger shortcuts when typing in inputs
    const target = event.target as HTMLElement;
    if (
      target.tagName === 'INPUT' ||
      target.tagName === 'TEXTAREA' ||
      target.isContentEditable
    ) {
      // Allow Ctrl+S even in inputs for saving
      if (!(event.ctrlKey && event.key === 's')) {
        return;
      }
    }

    for (const shortcut of shortcuts) {
      const ctrlMatch = shortcut.ctrl ? event.ctrlKey || event.metaKey : !event.ctrlKey && !event.metaKey;
      const shiftMatch = shortcut.shift ? event.shiftKey : !event.shiftKey;
      const altMatch = shortcut.alt ? event.altKey : !event.altKey;
      const keyMatch = event.key.toLowerCase() === shortcut.key.toLowerCase();

      if (ctrlMatch && shiftMatch && altMatch && keyMatch) {
        event.preventDefault();
        shortcut.action();
        break;
      }
    }

    // ESC to close modals/dialogs
    if (event.key === 'Escape') {
      dispatchEvent(new CustomEvent('close-all-modals'));
    }
  };

  const enableShortcuts = () => {
    document.addEventListener('keydown', handleKeyDown);
  };

  const disableShortcuts = () => {
    document.removeEventListener('keydown', handleKeyDown);
  };

  // Auto-enable on mount
  onMounted(() => {
    enableShortcuts();
  });

  onUnmounted(() => {
    disableShortcuts();
  });

  const getShortcutsByCategory = (category: KeyboardShortcut['category']) => {
    return shortcuts.filter(s => s.category === category);
  };

  const getAllShortcuts = () => shortcuts;

  const formatShortcut = (shortcut: KeyboardShortcut): string => {
    const parts: string[] = [];
    
    if (shortcut.ctrl || shortcut.meta) {
      parts.push(navigator.platform.includes('Mac') ? '⌘' : 'Ctrl');
    }
    if (shortcut.shift) parts.push('Shift');
    if (shortcut.alt) parts.push(navigator.platform.includes('Mac') ? '⌥' : 'Alt');
    parts.push(shortcut.key.toUpperCase());

    return parts.join(' + ');
  };

  return {
    shortcuts: getAllShortcuts(),
    getShortcutsByCategory,
    formatShortcut,
    enableShortcuts,
    disableShortcuts
  };
}
