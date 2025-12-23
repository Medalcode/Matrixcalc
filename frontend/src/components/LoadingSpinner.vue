<template>
  <div :class="['loading-spinner', sizeClass]">
    <svg class="spinner" viewBox="0 0 50 50">
      <circle
        class="path"
        cx="25"
        cy="25"
        r="20"
        fill="none"
        stroke-width="4"
      ></circle>
    </svg>
    <p v-if="message" class="loading-message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface Props {
  size?: "sm" | "md" | "lg";
  message?: string;
}

const props = withDefaults(defineProps<Props>(), {
  size: "md",
});

const sizeClass = computed(() => `size-${props.size}`);
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.spinner {
  animation: rotate 2s linear infinite;
}

.size-sm .spinner {
  width: 24px;
  height: 24px;
}

.size-md .spinner {
  width: 40px;
  height: 40px;
}

.size-lg .spinner {
  width: 60px;
  height: 60px;
}

.path {
  stroke: #3b82f6;
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}

.loading-message {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
  text-align: center;
}

:global(.dark) .path {
  stroke: #60a5fa;
}

:global(.dark) .loading-message {
  color: #9ca3af;
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
}
</style>
