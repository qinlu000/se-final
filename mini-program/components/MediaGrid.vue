<template>
  <view :class="['media-grid', gridClass]">
    <view
      v-for="(item, index) in media"
      :key="index"
      class="media-item"
      @click="preview(index)"
    >
      <image :src="item" mode="aspectFill" />
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  media: {
    type: Array,
    default: () => [],
  },
})

const gridClass = computed(() => {
  const count = props.media.length
  if (count === 1) return 'single'
  if (count === 2 || count === 4) return 'two-col'
  return 'three-col'
})

const preview = (index) => {
  uni.previewImage({
    urls: props.media,
    current: index,
  })
}
</script>

<style scoped>
.media-grid {
  display: grid;
  gap: 8rpx;
  margin-top: 12rpx;
}

.media-grid.single {
  grid-template-columns: repeat(1, minmax(0, 1fr));
}

.media-grid.two-col {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.media-grid.three-col {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.media-item {
  position: relative;
  overflow: hidden;
  border-radius: 12rpx;
  background: #f5f5f5;
}

.media-item image {
  width: 100%;
  height: 100%;
  min-height: 180rpx;
  display: block;
}

.media-grid.single .media-item image {
  min-height: 320rpx;
  border-radius: 16rpx;
}
</style>
