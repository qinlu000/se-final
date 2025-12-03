<template>
  <div class="page">
    <div class="cards">
      <el-card class="card gradient-1">
        <div class="stat-title">总用户</div>
        <div class="stat-value">{{ stats.total_users }}</div>
      </el-card>
      <el-card class="card gradient-2">
        <div class="stat-title">总内容</div>
        <div class="stat-value">{{ stats.total_posts }}</div>
      </el-card>
      <el-card class="card gradient-3">
        <div class="stat-title">今日活跃</div>
        <div class="stat-value">{{ todayActive }}</div>
      </el-card>
      <el-card class="card gradient-4">
        <div class="stat-title">互动总量</div>
        <div class="stat-value">{{ totalInteractions }}</div>
      </el-card>
    </div>

    <div class="charts-row">
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>活跃趋势</span>
            <el-tag size="small" effect="plain">近7天</el-tag>
          </div>
        </template>
        <div ref="lineRef" class="chart"></div>
      </el-card>

      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>内容类型分布</span>
            <el-tag size="small" effect="plain">实时</el-tag>
          </div>
        </template>
        <div ref="pieRef" class="chart"></div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, reactive, ref, watch, computed } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'

import api from '../api'

interface DashboardStats {
  total_users: number
  total_posts: number
  daily_active: { date: string; active: number }[]
  content_type_distribution: { name: string; value: number }[]
}

const stats = reactive<DashboardStats>({
  total_users: 0,
  total_posts: 0,
  daily_active: [],
  content_type_distribution: [],
})

const todayActive = computed(() => {
  if (stats.daily_active.length > 0) {
    return stats.daily_active[stats.daily_active.length - 1].active
  }
  return 0
})

// Mock interaction count based on posts (since we don't have a direct API for it yet)
const totalInteractions = computed(() => {
  return stats.total_posts * 5 + stats.total_users * 2 // Simplified estimation
})

const lineRef = ref<HTMLDivElement>()
const pieRef = ref<HTMLDivElement>()
let lineChart: echarts.ECharts | null = null
let pieChart: echarts.ECharts | null = null

const fetchStats = async () => {
  try {
    const res = await api.get<DashboardStats>('/stats/dashboard')
    Object.assign(stats, res.data)
  } catch (error: any) {
    const detail = error?.response?.data?.detail || '获取统计数据失败'
    ElMessage.error(detail)
  }
}

const renderCharts = () => {
  if (lineRef.value) {
    if (lineChart) lineChart.dispose()
    lineChart = echarts.init(lineRef.value)
    lineChart.setOption({
      tooltip: { trigger: 'axis' },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: { 
        type: 'category', 
        data: stats.daily_active.map((d) => d.date.slice(5)), // Show MM-DD
        axisLine: { lineStyle: { color: '#e5e7eb' } },
        axisLabel: { color: '#6b7280' }
      },
      yAxis: { 
        type: 'value',
        splitLine: { lineStyle: { type: 'dashed', color: '#f3f4f6' } }
      },
      series: [
        {
          name: '活跃用户',
          type: 'line',
          data: stats.daily_active.map((d) => d.active),
          smooth: true,
          symbolSize: 8,
          itemStyle: { color: '#3b82f6' },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
              { offset: 1, color: 'rgba(59, 130, 246, 0)' }
            ])
          },
        },
      ],
    })
  }

  if (pieRef.value) {
    if (pieChart) pieChart.dispose()
    pieChart = echarts.init(pieRef.value)
    
    // Map backend types to display names
    const typeMap: Record<string, string> = {
      'text': '纯文本',
      'image': '图文',
      'video': '视频'
    }

    const pieData = stats.content_type_distribution.map(item => ({
      name: typeMap[item.name] || item.name,
      value: item.value
    }))

    pieChart.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: '0%', left: 'center' },
      series: [
        {
          name: '内容类型',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: { show: false, position: 'center' },
          emphasis: {
            label: { show: true, fontSize: 20, fontWeight: 'bold' }
          },
          data: pieData.length ? pieData : [{ value: 0, name: '暂无数据' }],
        },
      ],
    })
  }
}

const resizeCharts = () => {
  lineChart?.resize()
  pieChart?.resize()
}

watch(
  () => [stats.daily_active, stats.content_type_distribution],
  () => {
    renderCharts()
  },
  { deep: true }
)

onMounted(async () => {
  await fetchStats()
  renderCharts()
  window.addEventListener('resize', resizeCharts)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeCharts)
  lineChart?.dispose()
  pieChart?.dispose()
})
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
}

.card {
  text-align: center;
  border: none;
  color: white;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-4px);
}

.gradient-1 { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); }
.gradient-2 { background: linear-gradient(135deg, #3b82f6 0%, #2dd4bf 100%); }
.gradient-3 { background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%); }
.gradient-4 { background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%); }

.stat-title {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: white;
}

.charts-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.chart-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart {
  width: 100%;
  height: 350px;
}

@media (max-width: 1024px) {
  .charts-row {
    grid-template-columns: 1fr;
  }
}
</style>
