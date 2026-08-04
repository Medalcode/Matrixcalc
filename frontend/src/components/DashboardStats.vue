<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="mb-6">
      <h3 class="text-lg font-medium text-gray-900">{{ t('stats.title') }}</h3>
      <p class="text-sm text-gray-500">Visualización de métricas del sistema</p>
    </div>

    <!-- Charts -->
    <div v-if="stats" class="space-y-6">
      <!-- Operations by Type - Pie Chart -->
      <div>
        <h4 class="text-sm font-medium text-gray-900 mb-4">{{ t('stats.charts.distribution') }}</h4>
        <div class="h-64 flex items-center justify-center">
          <Pie v-if="pieChartData" :data="pieChartData" :options="pieChartOptions" />
          <p v-else class="text-gray-400 text-sm">No hay datos suficientes</p>
        </div>
      </div>

      <!-- Operations Timeline - Line Chart -->
      <div>
        <h4 class="text-sm font-medium text-gray-900 mb-4">{{ t('stats.charts.timeline') }}</h4>
        <div class="h-64">
          <Line v-if="lineChartData" :data="lineChartData" :options="lineChartOptions" />
          <p v-else class="text-center text-gray-400 text-sm py-20">No hay datos de timeline</p>
        </div>
      </div>

      <!-- Average Execution Time by Operation -->
      <div>
        <h4 class="text-sm font-medium text-gray-900 mb-4">{{ t('stats.charts.avgTime') }}</h4>
        <div class="h-64">
          <Bar v-if="barChartData" :data="barChartData" :options="barChartOptions" />
          <p v-else class="text-center text-gray-400 text-sm py-20">No hay datos disponibles</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStatsStore } from '@/stores/statsStore'
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  type ChartOptions
} from 'chart.js'
import { Pie, Line, Bar } from 'vue-chartjs'
import type { OperationType } from '@/types/matrix'

// Register Chart.js components
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement
)

const { t } = useI18n()
const statsStore = useStatsStore()
const { stats } = storeToRefs(statsStore)

const getOperationName = (type: OperationType): string => {
  return t(`stats.operationTypes.${type}`)
}

const operationColors: Record<OperationType, string> = {
  'SUM': '#3b82f6',
  'SUBTRACT': '#ef4444',
  'MULTIPLY': '#10b981',
  'INVERSE': '#f59e0b',
  'DETERMINANT': '#8b5cf6',
  'TRANSPOSE': '#ec4899',
  'RANK': '#6366f1',
  'EIGEN': '#14b8a6',
  'SVD': '#a855f7',
  'QR': '#f97316',
  'CHOLESKY': '#06b6d4'
}

// Pie Chart Data
const pieChartData = computed(() => {
  if (!stats.value || !stats.value.operations_by_type.length) return null

  const labels = stats.value.operations_by_type.map(op => getOperationName(op.operation_type))
  const data = stats.value.operations_by_type.map(op => op.count)
  const backgroundColor = stats.value.operations_by_type.map(op => operationColors[op.operation_type])

  return {
    labels,
    datasets: [
      {
        data,
        backgroundColor,
        borderWidth: 2,
        borderColor: '#fff'
      }
    ]
  }
})

const pieChartOptions: ChartOptions<'pie'> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom'
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const label = context.label || ''
          const value = context.parsed || 0
          const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0)
          const percentage = ((value / total) * 100).toFixed(1)
          return `${label}: ${value} (${percentage}%)`
        }
      }
    }
  }
}

// Line Chart Data
const lineChartData = computed(() => {
  if (!stats.value || !stats.value.operations_timeline.length) return null

  const labels = stats.value.operations_timeline.map(item => {
    const date = new Date(item.date)
    return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' })
  })
  const data = stats.value.operations_timeline.map(item => item.count)

  return {
    labels,
    datasets: [
      {
        label: 'Operaciones',
        data,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.3,
        fill: true
      }
    ]
  }
})

const lineChartOptions: ChartOptions<'line'> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      mode: 'index',
      intersect: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        precision: 0
      }
    }
  }
}

// Bar Chart Data
const barChartData = computed(() => {
  if (!stats.value || !stats.value.operations_by_type.length) return null

  const labels = stats.value.operations_by_type.map(op => getOperationName(op.operation_type))
  const data = stats.value.operations_by_type.map(op => op.avg_time)
  const backgroundColor = stats.value.operations_by_type.map(op => operationColors[op.operation_type])

  return {
    labels,
    datasets: [
      {
        label: 'Tiempo Promedio (ms)',
        data,
        backgroundColor,
        borderWidth: 0
      }
    ]
  }
})

const barChartOptions: ChartOptions<'bar'> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const value = context.parsed.y
          if (value === null) return ''
          return `Tiempo promedio: ${value.toFixed(2)}ms`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Milisegundos'
      }
    }
  }
}

</script>
