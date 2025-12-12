<template>
  <view class="ai-card">
    <view class="header">
      <text class="title">AI解读</text>
      <text class="status">Grok-style</text>
    </view>
    <view class="summary">
      <text class="summary-text">{{ displaySummary }}</text>
    </view>
    <view v-if="tags?.length" class="tags">
      <text v-for="tag in tags" :key="tag" class="tag">#{{ tag }}</text>
    </view>
    <view v-if="suggestions?.length" class="replies">
      <text class="reply-label">快速回复</text>
      <view class="chips">
        <view
          v-for="(item, idx) in suggestions"
          :key="idx"
          class="chip"
          @click="$emit('select-reply', item)"
        >
          {{ item }}
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  summary: {
    type: String,
    default: '',
  },
  tags: {
    type: Array,
    default: () => [],
  },
  suggestions: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['select-reply'])

const displaySummary = ref('')

const runTypewriter = () => {
  displaySummary.value = ''
  const text = props.summary || ''
  let idx = 0
  const timer = setInterval(() => {
    displaySummary.value = text.slice(0, idx)
    idx += 1
    if (idx > text.length) {
      clearInterval(timer)
    }
  }, 12)
}

watch(
  () => props.summary,
  () => {
    runTypewriter()
  },
  { immediate: true }
)

onMounted(runTypewriter)
</script>

<style scoped>
.ai-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: var(--border-thin);
  border-radius: 16rpx;
  padding: 24rpx;
  margin-top: 24rpx;
  animation: slideDown 0.3s ease-out;
  box-shadow: var(--shadow-hard);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12rpx;
}

.title {
  font-weight: 900;
  font-size: 30rpx;
}

.status {
  font-size: 22rpx;
  color: #333;
}

.summary {
  margin-top: 6rpx;
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
