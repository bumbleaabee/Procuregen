<template>
  <div class="step">
    <div class="step-head">
      <h2>合规风险预审</h2>
      <p>共检测到 {{ store.riskReport?.risks?.length || 0 }} 个风险项</p>
    </div>
    <RadarChart :data="radarData" v-if="store.riskReport?.risks?.length" />
    <div v-if="store.riskReport?.risks?.length" class="risk-list">
      <div v-for="(risk, idx) in store.riskReport.risks" :key="idx" class="risk-card" :class="'risk-' + risk.level">
        <div class="risk-header">
          <span class="risk-badge" :class="'badge-' + risk.level">{{ levelMap[risk.level] || risk.level }}</span>
          <span class="risk-type">{{ risk.type }}</span>
        </div>
        <p class="risk-msg">{{ risk.message }}</p>
        <p class="risk-sug">{{ risk.suggestion }}</p>
      </div>
    </div>
    <div v-else class="empty-state">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.2"/><polyline points="8 12 11 15 16 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <p>未检测到风险，文件合规性良好</p>
    </div>
    <div class="step-actions">
      <button class="apple-btn apple-btn-secondary" @click="store.currentStep = 1" :disabled="store.loading">返回修改</button>
      <button class="apple-btn apple-btn-primary" @click="store.doGenerate()" :disabled="store.loading" style="padding:12px 24px;font-size:15px;">
        确认并生成文档
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><polyline points="9 18 15 12 9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useGenerateStore } from '../stores/generate'
import RadarChart from './RadarChart.vue'

const store = useGenerateStore()
const levelMap = { high: '高风险', medium: '中风险', low: '低风险' }

const radarData = computed(() => {
  const risks = store.riskReport?.risks || []
  if (!risks.length) return []
  const cats = {}
  risks.forEach(r => { const key = r.type || '其他'; cats[key] = (cats[key] || 0) + 1 })
  return Object.entries(cats).map(([label, count]) => ({ label, value: Math.min(count * 25, 100) })).slice(0, 6)
})
</script>

<style scoped>
.step-head { text-align: center; margin-bottom: 24px; }
.step-head h2 { font-size: 24px; font-weight: 650; letter-spacing: -0.5px; }
.step-head p { font-size: 14px; color: var(--text-secondary); margin-top: 6px; }
.risk-list { display: flex; flex-direction: column; gap: 12px; }
.risk-card { padding: 20px; border-radius: var(--radius); border: 0.5px solid var(--border); }
.risk-high { border-left: 3px solid #ff3b30; background: #ff3b3006; }
.risk-medium { border-left: 3px solid #f5a623; background: #f5a62306; }
.risk-low { border-left: 3px solid #34c759; background: #34c75906; }
.risk-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.risk-badge { font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 100px; }
.badge-high { background: #ff3b3020; color: #ff3b30; }
.badge-medium { background: #f5a62320; color: #b87a14; }
.badge-low { background: #34c75920; color: #34c759; }
.risk-type { font-weight: 550; color: var(--text-primary); }
.risk-msg { font-size: 13px; color: var(--text-secondary); line-height: 1.6; }
.risk-sug { font-size: 13px; color: var(--accent); margin-top: 6px; line-height: 1.6; }
.empty-state { text-align: center; padding: 40px 0; color: var(--text-tertiary); }
.empty-state svg { color: #34c759; margin-bottom: 12px; }
.step-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 28px; }
</style>
