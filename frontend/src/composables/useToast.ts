import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface Toast {
  id: number
  message: string
  type: ToastType
  duration: number
}

const toasts = ref<Toast[]>([])
const toastTimeouts = new Map<number, ReturnType<typeof setTimeout>>()
let toastIdCounter = 0

export function useToast() {
  const show = (message: string, type: ToastType = 'info', duration = 3000) => {
    const id = toastIdCounter++
    const toast: Toast = { id, message, type, duration }
    
    toasts.value.push(toast)
    
    if (duration > 0) {
      const timeoutId = setTimeout(() => {
        remove(id)
      }, duration)
      toastTimeouts.set(id, timeoutId)
    }
    
    return id
  }
  
  const remove = (id: number) => {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
    const timeoutId = toastTimeouts.get(id)
    if (timeoutId) {
      clearTimeout(timeoutId)
      toastTimeouts.delete(id)
    }
  }
  
  const success = (message: string, duration = 3000) => show(message, 'success', duration)
  const error = (message: string, duration = 5000) => show(message, 'error', duration)
  const warning = (message: string, duration = 4000) => show(message, 'warning', duration)
  const info = (message: string, duration = 3000) => show(message, 'info', duration)
  
  return {
    toasts,
    show,
    remove,
    success,
    error,
    warning,
    info
  }
}
