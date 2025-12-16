<template>
  <view v-if="visible" class="popup-mask" @click="handleMaskClick">
    <view 
      class="popup-content" 
      :class="[type, { 'show': visible }]" 
      @click.stop
    >
      <!-- Modal: Title + Content + Buttons -->
      <block v-if="type === 'modal'">
        <view class="modal-header">
          <text class="modal-title">{{ title }}</text>
        </view>
        <view class="modal-body">
          <text class="modal-text">{{ content }}</text>
        </view>
        <view class="modal-footer">
          <button class="neu-btn cancel-btn" @click="onCancel">{{ cancelText }}</button>
          <button class="neu-btn confirm-btn" @click="onConfirm">{{ confirmText }}</button>
        </view>
      </block>

      <!-- ActionSheet: List of Options + Cancel -->
      <block v-if="type === 'sheet'">
        <view class="sheet-header" v-if="title">
          <text class="sheet-title">{{ title }}</text>
        </view>
        <view class="sheet-list">
          <view 
            v-for="(item, index) in actions" 
            :key="index" 
            class="sheet-item neu-btn"
            @click="onAction(index)"
          >
            {{ item }}
          </view>
        </view>
        <view class="sheet-cancel">
          <button class="neu-btn cancel-btn full" @click="onCancel">取消</button>
        </view>
      </block>
    </view>
  </view>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  visible: Boolean,
  type: {
    type: String,
    default: 'modal' // 'modal' | 'sheet'
  },
  title: String,
  content: String, // For modal
  actions: Array, // For sheet ['Option A', 'Option B']
  confirmText: {
    type: String,
    default: '确定'
  },
  cancelText: {
    type: String,
    default: '取消'
  }
})

const emit = defineEmits(['update:visible', 'confirm', 'cancel', 'action'])

const close = () => {
  emit('update:visible', false)
}

const handleMaskClick = () => {
  close()
}

const onCancel = () => {
  close()
  emit('cancel')
}

const onConfirm = () => {
  close()
  emit('confirm')
}

const onAction = (index) => {
  close()
  emit('action', index)
}
</script>

<style scoped>
.popup-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(4px);
}

.popup-content {
  background: var(--c-white);
  border: var(--border-thick);
  box-shadow: 8px 8px 0px #000;
  border-radius: var(--radius-m);
  overflow: hidden;
  transition: all 0.2s ease;
}

/* --- Modal Styles --- */
.popup-content.modal {
  width: 560rpx;
  animation: popIn 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.modal-header {
  padding: 32rpx 32rpx 16rpx;
  text-align: center;
}

.modal-title {
  font-size: 36rpx;
  font-weight: 900;
}

.modal-body {
  padding: 0 32rpx 40rpx;
  text-align: center;
}

.modal-text {
  font-size: 30rpx;
  color: #333;
  line-height: 1.5;
}

.modal-footer {
  display: flex;
  padding: 24rpx;
  gap: 24rpx;
  background: var(--c-bg); /* Separator feel */
  border-top: var(--border-thick);
}

.cancel-btn {
  flex: 1;
  background: #fff !important;
  color: #000;
}

.confirm-btn {
  flex: 1;
  background: var(--c-yellow) !important;
}

/* --- Sheet Styles (Bottom Slide) --- */
.popup-content.sheet {
  position: fixed;
  bottom: 40rpx;
  left: 40rpx;
  right: 40rpx;
  width: auto;
  border-radius: var(--radius-m);
  animation: slideUp 0.2s ease-out;
  padding: 24rpx;
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.sheet-header {
  text-align: center;
  padding: 16rpx 0;
  font-weight: 700;
  font-size: 30rpx;
  color: #666;
  border-bottom: 2rpx dashed #000;
  margin-bottom: 8rpx;
}

.sheet-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.sheet-item {
  height: 88rpx;
  line-height: 88rpx;
  text-align: center;
  background: #fff;
  font-size: 32rpx;
}

.sheet-item:active {
  background: var(--c-yellow);
}

.sheet-cancel {
  margin-top: 16rpx;
  border-top: 2rpx dashed #000; /* Separator */
  padding-top: 16rpx;
}

.full {
  width: 100%;
  height: 88rpx;
  line-height: 88rpx;
}

@keyframes popIn {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes slideUp {
  from { transform: translateY(100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
