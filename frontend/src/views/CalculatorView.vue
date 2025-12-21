<template>
  <div class="min-h-screen bg-gray-50 py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">{{ t('calculator.title') }}</h1>
        <p class="mt-2 text-sm text-gray-600">
          Crea matrices y realiza operaciones matriciales
        </p>
      </div>

      <!-- Tab Navigation -->
      <div class="mb-6">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button
              @click="activeTab = 'editor'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                activeTab === 'editor'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ t('calculator.editor.title') }}
            </button>
            <button
              @click="activeTab = 'operations'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                activeTab === 'operations'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ t('calculator.operations.title') }}
            </button>
            <button
              @click="activeTab = 'backup'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                activeTab === 'backup'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ t('calculator.backup.title') }}
            </button>
          </nav>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column: Matrices List -->
        <div class="lg:col-span-1">
          <MatrixList
            @view="handleViewMatrix"
            @edit="handleEditMatrix"
            @select="handleSelectMatrix"
          />
        </div>

        <!-- Right Column: Active Tab Content -->
        <div class="lg:col-span-2">
          <!-- Editor Tab -->
          <div v-if="activeTab === 'editor'">
            <MatrixEditor
              :matrix="editingMatrix"
              @saved="handleMatrixSaved"
              @cancelled="handleEditCancelled"
            />
          </div>

          <!-- Operations Tab -->
          <div v-else-if="activeTab === 'operations'">
            <OperationPanel
              @result="handleOperationResult"
              @viewMatrix="handleViewMatrix"
            />
            
            <!-- Result Viewer -->
            <div v-if="operationResult" class="mt-6">
              <ResultViewer
                :matrix="operationResult.result"
                :operation="operationResult"
                :on-close="() => operationResult = null"
              />
            </div>
          </div>

          <!-- Backup Tab -->
          <div v-else-if="activeTab === 'backup'">
            <BackupManager @imported="handleMatrixImported" />
          </div>
        </div>
      </div>

      <!-- View Matrix Modal -->
      <div
        v-if="viewingMatrix"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
        @click.self="viewingMatrix = null"
      >
        <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-auto">
          <ResultViewer
            :matrix="viewingMatrix"
            :on-close="() => viewingMatrix = null"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
import MatrixEditor from '@/components/MatrixEditor.vue'
import MatrixList from '@/components/MatrixList.vue'
import OperationPanel from '@/components/OperationPanel.vue'
import ResultViewer from '@/components/ResultViewer.vue'
import BackupManager from '@/components/BackupManager.vue'
import type { Matrix, Operation } from '@/types/matrix'

const activeTab = ref<'editor' | 'operations' | 'backup'>('editor')
const editingMatrix = ref<Matrix | undefined>(undefined)
const viewingMatrix = ref<Matrix | null>(null)
const operationResult = ref<Operation | null>(null)

function handleEditMatrix(matrix: Matrix) {
  editingMatrix.value = matrix
  activeTab.value = 'editor'
}

function handleViewMatrix(matrix: Matrix) {
  viewingMatrix.value = matrix
}

function handleSelectMatrix(matrix: Matrix) {
  // This will be handled by the MatrixList component emitting to OperationPanel
  activeTab.value = 'operations'
}

function handleMatrixSaved(matrix: Matrix) {
  editingMatrix.value = undefined
  // Optionally show a success notification
}

function handleEditCancelled() {
  editingMatrix.value = undefined
}

function handleOperationResult(operation: Operation) {
  operationResult.value = operation
}

function handleMatrixImported(matrix: Matrix) {
  // Optionally switch to editor or show notification
  activeTab.value = 'editor'
}
</script>
