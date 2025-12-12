<template>
  <view class="ai-card" :style="cardStyle">
    <view class="header">
      <view class="title-row">
        <text class="title">✨ AI 解读</text>
      </view>
      <view class="actions">
        <view v-if="vibe" class="vibe-chip" :style="{ background: vibe.color || '#ffe600' }">
          <text class="vibe-emoji">{{ vibe.emoji }}</text>
          <text class="vibe-label">{{ vibe.label }}</text>
        </view>
        <view class="tab" :class="{ active: activeTab === 'summary' }" @click="activeTab = 'summary'">摘要</view>
        <view class="tab" :class="{ active: activeTab === 'translate' }" @click="handleTranslateTab">翻译</view>
      </view>
    </view>

    <view v-if="activeTab === 'summary'" class="body">
      <text class="summary-text">{{ displaySummary }}</text>
    </view>
    <view v-else class="body">
      <text v-if="translateLoading" class="summary-text">Translating...</text>
      <text v-else-if="translatedContent" class="summary-text">{{ translatedContent }}</text>
      <text v-else class="summary-text">暂无翻译</text>
    </view>

    <view v-if="tags.length" class="tags">
      <text v-for="tag in tags" :key="tag" class="tag">#{{ tag }}</text>
    </view>

    <view v-if="suggestions.length" class="replies">
      <text class="reply-label">快速回复</text>
      <view class="chips">
        <view
          v-for="(item, idx) in suggestions"
          :key="idx"
          class="chip"
          @click="$emit('reply', item)"
        >
          {{ item }}
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { askAI } from '../api/ai'

const props = defineProps({
  content: {
    type: String,
    required: true,
  },
  tone: {
    type: String,
    default: 'friendly',
  },
})

const emit = defineEmits(['reply'])

const activeTab = ref('summary')
const summary = ref('')
const translatedContent = ref('')
const tags = ref([])
const suggestions = ref([])
const vibe = ref(null)
const displaySummary = ref('')
const loading = ref(false)
const translateLoading = ref(false)

const cardStyle = computed(() => {
  const color = vibe.value?.color || 'rgba(255,255,255,0.8)'
  return `background: ${color}22; border: var(--border-thick); box-shadow: var(--shadow-hard);`
})

const runTypewriter = () => {
  displaySummary.value = ''
  const text = summary.value || ''
  let idx = 0
  const timer = setInterval(() => {
    displaySummary.value = text.slice(0, idx)
    idx += 1
    if (idx > text.length) clearInterval(timer)
  }, 12)
}

const fetchSummary = async () => {
  if (loading.value) return
  loading.value = true
  try {
    const res = await askAI({
      content: props.content,
      mode: 'summary',
      tone: props.tone,
      include_tags: true,
    })
    if (res?.status === 'sensitive') {
      summary.value = '内容包含敏感信息'
      return
    }
    summary.value = res?.summary || ''
    tags.value = res?.tags || []
    suggestions.value = res?.suggestions || []
    vibe.value = res?.vibe || null
    if (res?.translated_content) {
      translatedContent.value = res.translated_content
    }
    runTypewriter()
  } catch (e) {
    summary.value = 'AI暂不可用'
  } finally {
    loading.value = false
  }
}

const fetchTranslate = async () => {
  if (translateLoading.value || translatedContent.value) return
  translateLoading.value = true
  try {
    const res = await askAI({
      content: props.content,
      mode: 'translate',
      target_lang: 'zh',
    })
    if (res?.status === 'sensitive') {
      translatedContent.value = '内容包含敏感信息'
      return
    }
    translatedContent.value = res?.translated_content || ''
  } catch (e) {
    translatedContent.value = '翻译失败'
  } finally {
    translateLoading.value = false
  }
}

const handleTranslateTab = () => {
  activeTab.value = 'translate'
  fetchTranslate()
}

watch(
  () => props.content,
  () => {
    summary.value = ''
    translatedContent.value = ''
    tags.value = []
    suggestions.value = []
    vibe.value = null
    activeTab.value = 'summary'
    fetchSummary()
  },
  { immediate: true }
)

onMounted(fetchSummary)
</script>

<style scoped>
.ai-card {
  backdrop-filter: blur(10px);
  border-radius: 16rpx;
  padding: 24rpx;
  margin-top: 24rpx;
  animation: slideDown 0.3s ease-out;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10rpx;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.title {
  font-weight: 900;
  font-size: 30rpx;
}

.actions {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.tab {
  padding: 10rpx 18rpx;
  border: var(--border-thick);
  border-radius: var(--radius-full);
  background: #ffffff;
  box-shadow: var(--shadow-hard);
  font-weight: 800;
}

.tab.active {
  background: var(--c-yellow);
}

.vibe-chip {
  display: inline-flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 12rpx;
  border: var(--border-thick);
  border-radius: 14rpx;
  box-shadow: var(--shadow-hard);
}

.vibe-emoji {
  font-size: 30rpx;
}

.vibe-label {
  font-weight: 800;
  font-size: 24rpx;
}

.body {
  margin-top: 16rpx;
}

.summary-text {
  font-family: 'DM Mono', monospace;
  color: #333;
  font-size: 28rpx;
  line-height: 1.6;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-top: 18rpx;
}

.tag {
  background: var(--c-yellow);
  border: 2rpx solid #000;
  border-radius: 12rpx;
  padding: 8rpx 14rpx;
  font-weight: 800;
}

.replies {
  margin-top: 18rpx;
}

.reply-label {
  font-size: 24rpx;
  font-weight: 800;
}

.chips {
  margin-top: 10rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
}

.chip {
  padding: 10rpx 16rpx;
  border-radius: 16rpx;
  border: var(--border-thick);
  background: #ffffff;
  box-shadow: var(--shadow-hard);
  font-size: 24rpx;
}

@keyframes slideDown {
  from {
    transform: translateY(-8rpx);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
