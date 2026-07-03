<template>
  <div class="score-card">
    <div class="score-ring">
      <svg width="120" height="120" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r="52" fill="none" stroke="var(--border)" stroke-width="6"/>
        <circle cx="60" cy="60" r="52" fill="none" :stroke="scoreColor" stroke-width="6"
          stroke-linecap="round" :stroke-dasharray="circumference" :stroke-dashoffset="offset"
          transform="rotate(-90 60 60)" style="transition: stroke-dashoffset 1.2s cubic-bezier(0.4,0,0.2,1)"
        />
      </svg>
      <div class="score-value" :style="{ color: scoreColor }">{{ score }}</div>
      <div class="score-unit">/ 100</div>
    </div>
    <div class="score-details">
      <div class="detail-item" v-for="d in details" :key="d.label">
        <div class="detail-label">{{ d.label }}</div>
        <div class="detail-bar-wrap">
          <div class="detail-bar" :style="{ width: d.value + '%', background: d.color || 'var(--accent)' }"></div>
        </div>
        <div class="detail-val">{{ d.value }}%</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  score: { type: Number, default: 85 },
  details: { type: Array, default: () => [] },
})

const circumference = 2 * Math.PI * 52
const offset = computed(() => circumference * (1 - props.score / 100))
const scoreColor = computed(() => {
  if (props.score >= 80) return '#34c759'
  if (props.score >= 60) return '#f5a623'
  return '#ff3b30'
})
</script>

<style scoped>
.score-card { display: flex; align-items: center; gap: 28px; padding: 16px 0; }
.score-ring { position: relative; flex-shrink: 0; width: 120px; height: 120px; display: flex; align-items: center; justify-content: center; }
.score-value { position: absolute; font-size: 32px; font-weight: 750; letter-spacing: -1px; }
.score-unit { position: absolute; bottom: 28px; font-size: 12px; color: var(--text-tertiary); }
.score-details { flex: 1; display: flex; flex-direction: column; gap: 10px; }
.detail-item { display: flex; align-items: center; gap: 10px; }
.detail-label { font-size: 12px; color: var(--text-secondary); width: 80px; text-align: right; flex-shrink: 0; }
.detail-bar-wrap { flex: 1; height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
.detail-bar { height: 100%; border-radius: 3px; transition: width 0.8s ease; }
.detail-val { font-size: 12px; color: var(--text-tertiary); width: 36px; }
</style>
