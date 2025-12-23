<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50 backdrop-blur-sm"
        @click.self="cancel"
      >
        <div
          class="bg-white dark:bg-gray-800 rounded-lg shadow-2xl max-w-md w-full overflow-hidden transform transition-all"
          @click.stop
        >
          <!-- Header -->
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <div class="flex items-center gap-3">
              <!-- Icon -->
              <div
                :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center',
                  iconColorClass,
                ]"
              >
                <component :is="iconComponent" class="w-6 h-6" />
              </div>

              <!-- Title -->
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                {{ title }}
              </h3>
            </div>
          </div>

          <!-- Body -->
          <div class="px-6 py-4">
            <p class="text-gray-600 dark:text-gray-300">
              {{ message }}
            </p>
          </div>

          <!-- Footer -->
          <div
            class="px-6 py-4 bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 flex gap-3 justify-end"
          >
            <button
              @click="cancel"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
            >
              {{ cancelText }}
            </button>
            <button
              @click="confirm"
              :class="[
                'px-4 py-2 text-sm font-medium text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors',
                confirmButtonClass,
              ]"
            >
              {{ confirmText }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from "vue";

export type ConfirmationType = "danger" | "warning" | "info" | "success";

interface Props {
  modelValue: boolean;
  title?: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  type?: ConfirmationType;
}

const props = withDefaults(defineProps<Props>(), {
  title: "Confirmación",
  confirmText: "Confirmar",
  cancelText: "Cancelar",
  type: "warning",
});

const emit = defineEmits<{
  "update:modelValue": [value: boolean];
  confirm: [];
  cancel: [];
}>();

const iconComponent = computed(() => {
  switch (props.type) {
    case "danger":
      return "svg";
    case "warning":
      return "svg";
    case "success":
      return "svg";
    case "info":
    default:
      return "svg";
  }
});

const iconColorClass = computed(() => {
  switch (props.type) {
    case "danger":
      return "bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400";
    case "warning":
      return "bg-yellow-100 dark:bg-yellow-900 text-yellow-600 dark:text-yellow-400";
    case "success":
      return "bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400";
    case "info":
    default:
      return "bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400";
  }
});

const confirmButtonClass = computed(() => {
  switch (props.type) {
    case "danger":
      return "bg-red-600 hover:bg-red-700 focus:ring-red-500";
    case "warning":
      return "bg-yellow-600 hover:bg-yellow-700 focus:ring-yellow-500";
    case "success":
      return "bg-green-600 hover:bg-green-700 focus:ring-green-500";
    case "info":
    default:
      return "bg-blue-600 hover:bg-blue-700 focus:ring-blue-500";
  }
});

function confirm() {
  emit("confirm");
  emit("update:modelValue", false);
}

function cancel() {
  emit("cancel");
  emit("update:modelValue", false);
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-active > div,
.modal-leave-active > div {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from > div,
.modal-leave-to > div {
  transform: scale(0.95) translateY(-20px);
  opacity: 0;
}
</style>
