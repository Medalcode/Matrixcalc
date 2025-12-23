import { ref } from 'vue'

export interface ConfirmationOptions {
  title?: string
  message: string
  confirmText?: string
  cancelText?: string
  type?: 'danger' | 'warning' | 'info' | 'success'
}

const isOpen = ref(false)
const options = ref<ConfirmationOptions>({
  message: '',
  title: 'Confirmación',
  confirmText: 'Confirmar',
  cancelText: 'Cancelar',
  type: 'warning'
})

let resolvePromise: ((value: boolean) => void) | null = null

export function useConfirmation() {
  const confirm = (opts: ConfirmationOptions): Promise<boolean> => {
    options.value = {
      title: opts.title || 'Confirmación',
      message: opts.message,
      confirmText: opts.confirmText || 'Confirmar',
      cancelText: opts.cancelText || 'Cancelar',
      type: opts.type || 'warning'
    }
    
    isOpen.value = true
    
    return new Promise<boolean>((resolve) => {
      resolvePromise = resolve
    })
  }
  
  const handleConfirm = () => {
    isOpen.value = false
    if (resolvePromise) {
      resolvePromise(true)
      resolvePromise = null
    }
  }
  
  const handleCancel = () => {
    isOpen.value = false
    if (resolvePromise) {
      resolvePromise(false)
      resolvePromise = null
    }
  }
  
  return {
    isOpen,
    options,
    confirm,
    handleConfirm,
    handleCancel
  }
}
