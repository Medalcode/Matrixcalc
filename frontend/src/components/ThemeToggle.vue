<template>
  <button
    @click="toggleTheme"
    class="theme-toggle"
    :title="getThemeLabel()"
    aria-label="Toggle theme"
  >
    <!-- Sun icon (light mode) -->
    <svg
      v-if="theme === 'light'"
      class="w-5 h-5"
      fill="currentColor"
      viewBox="0 0 20 20"
    >
      <path
        fill-rule="evenodd"
        d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
        clip-rule="evenodd"
      />
    </svg>

    <!-- Moon icon (dark mode) -->
    <svg
      v-else-if="theme === 'dark'"
      class="w-5 h-5"
      fill="currentColor"
      viewBox="0 0 20 20"
    >
      <path
        d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"
      />
    </svg>

    <!-- Auto icon -->
    <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
      <path
        fill-rule="evenodd"
        d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
        clip-rule="evenodd"
      />
    </svg>

    <span class="theme-label">{{ getThemeLabel() }}</span>
  </button>
</template>

<script setup lang="ts">
import { useTheme } from "@/composables/useTheme";

const { theme, toggleTheme } = useTheme();

const getThemeLabel = () => {
  switch (theme.value) {
    case "light":
      return "Light";
    case "dark":
      return "Dark";
    case "auto":
      return "Auto";
    default:
      return "Theme";
  }
};
</script>

<style scoped>
.theme-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  color: #6b7280;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-toggle:hover {
  color: #374151;
  background: #f9fafb;
  border-color: #d1d5db;
}

.theme-toggle:focus {
  outline: none;
  ring: 2px;
  ring-color: #3b82f6;
  ring-offset: 2px;
}

.theme-label {
  min-width: 3rem;
  text-align: left;
}

/* Dark mode */
:global(.dark) .theme-toggle {
  color: #9ca3af;
  border-color: #374151;
}

:global(.dark) .theme-toggle:hover {
  color: #e5e7eb;
  background: #1f2937;
  border-color: #4b5563;
}

@media (max-width: 640px) {
  .theme-label {
    display: none;
  }

  .theme-toggle {
    padding: 0.5rem;
  }
}
</style>
