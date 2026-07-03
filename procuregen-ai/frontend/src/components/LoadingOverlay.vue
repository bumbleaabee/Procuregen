<template>
  <Teleport to="body">
    <Transition name="loading">
      <div v-if="visible" class="loading-overlay">
        <div class="loading-card">
          <div class="loading-icon">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <circle cx="24" cy="24" r="20" stroke="var(--border)" stroke-width="2"/>
              <path d="M24 4a20 20 0 0117.3 10.9" stroke="var(--accent)" stroke-width="2.5" stroke-linecap="round">
                <animateTransform attributeName="transform" type="rotate" values="0 24 24;360 24 24" dur="1s" repeatCount="indefinite"/>
              </path>
            </svg>
          </div>
          <div class="loading-status">{{ messages[currentMsg] }}</div>
          <div class="loading-dots">
            <span v-for="i in 3" :key="i" class="dot" :style="{ animationDelay: i * 0.15 + 's' }"></span>
          </div>
          <div class="loading-progress">
            <div class="progress-bar" :style="{ width: progress + '%' }"></div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'

const props = defineProps({
  visible: Boolean,
  status: { type: String, default: 'processing' }
})

const messages = {
  parsing: ['正在理解采购需求...', '提取关键参数中...', 'AI 正在分析文本结构...', '识别采购类型与预算...'],
  risk: ['正在执行合规检查...', '匹配风险规则库...', '生成风险解释...', '评估风险等级...'],
  generating: ['正在组装文档模板...', '渲染合同条款...', '生成 Word 文档...', '准备下载文件...'],
  processing: ['AI 正在处理...', '请稍候...', '模型推理中...', '即将完成...'],
}

const currentMsg = ref(0)
let timer = null

watch(() => props.visible, (v) => {
  if (v) {
    currentMsg.value = 0
    timer = setInterval(() => {
      const list = messages[props.status] || messages.processing
      currentMsg.value = (currentMsg.value + 1) % list.length
    }, 2000)
  } else {
    clearInterval(timer)
  }
})

onUnmounted(() => clearInterval(timer))

// 模拟进度
import { computed } from 'vue'
const progress = computed(() => Math.min(currentMsg.value * 25 + 15, 90))
</script>

<style scoped>
.loading-overlay {
  position: fixed; inset: 0; z-index: 99999;
  background: rgba(0,0,0,0.3);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center;
}
.loading-card {
  padding: 40px 48px; border-radius: 24px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 0.5px solid var(--border);
  box-shadow: var(--shadow-lg);
  text-align: center; min-width: 320px;
}
.loading-icon { margin-bottom: 20px; }
.loading-status {
  font-size: 15px; font-weight: 550; color: var(--text-primary);
  margin-bottom: 16px; letter-spacing: -0.2px; min-height: 22px;
}
.loading-dots { display: flex; justify-content: center; gap: 6px; margin-bottom: 20px; }
.dot {
  width: 6px; height: 6px; border-radius: 50%; background: var(--accent);
  animation: dotPulse 1.2s ease-in-out infinite;
}
@keyframes dotPulse { 0%,100% { opacity: 0.2; transform: scale(0.8); } 50% { opacity: 1; transform: scale(1.2); } }
.loading-progress { height: 3px; background: var(--border); border-radius: 2px; overflow: hidden; }
.progress-bar {
  height: 100%; background: var(--accent); border-radius: 2px;
  transition: width 0.5s ease;
}

.loading-enter-active { transition: all 0.3s ease-out; }
.loading-leave-active { transition: all 0.25s ease-in; }
.loading-enter-from { opacity: 0; }
.loading-enter-from .loading-card { transform: scale(0.9); opacity: 0; }
.loading-leave-to { opacity: 0; }
.loading-leave-to .loading-card { transform: scale(0.9); opacity: 0; }
</style>
