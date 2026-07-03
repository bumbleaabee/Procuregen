<template>
  <div class="step">
    <div class="step-head">
      <div class="success-icon">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="11" fill="#34c75920" stroke="#34c759" stroke-width="1.5"/><polyline points="7 12 10.5 15.5 17 9" stroke="#34c759" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <h2>文档生成完成</h2>
      <p>文件：{{ store.generateResult?.file_name || '' }}</p>
    </div>

    <QualityScore :score="qualityScore" :details="scoreDetails" />

    <div v-if="store.selectedClauses?.length" class="section">
      <h3 class="section-title">推荐合同条款</h3>
      <div v-for="clause in store.selectedClauses" :key="clause.clause_id || clause.title" class="clause-card">
        <h4>{{ clause.title }}</h4>
        <p class="clause-text">{{ (clause.content || '').slice(0, 200) }}{{ (clause.content || '').length > 200 ? '...' : '' }}</p>
        <p class="clause-reason">{{ clause.reason }}</p>
      </div>
    </div>

    <div class="section">
      <div class="section-header">
        <h3 class="section-title">文档预览</h3>
        <button class="apple-btn apple-btn-secondary copy-btn" @click="copyPreview">复制</button>
      </div>
      <div class="preview-box">{{ store.generateResult?.preview || '暂无预览' }}</div>
    </div>

    <div class="step-actions">
      <button class="apple-btn apple-btn-secondary" @click="store.reset()">新建文件</button>
      <button class="apple-btn apple-btn-primary dl-btn" @click="downloadDoc">下载 Word 文档</button>
      <router-link to="/history" class="apple-btn apple-btn-secondary">历史记录</router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useGenerateStore } from '../stores/generate'
import { ElMessage } from 'element-plus'
import QualityScore from './QualityScore.vue'

const store = useGenerateStore()

const qualityScore = computed(() => {
  const risks = store.riskReport?.risks?.length || 0
  const clauses = store.selectedClauses?.length || 0
  const missing = store.parsedSpec?.missing_fields?.length || 0
  const score = 85 - risks * 8 - missing * 10 + clauses * 2
  return Math.max(30, Math.min(100, Math.round(score)))
})

const scoreDetails = computed(() => {
  const risks = store.riskReport?.risks?.length || 0
  const clauses = store.selectedClauses?.length || 0
  const missing = store.parsedSpec?.missing_fields?.length || 0
  return [
    { label: '完整性', value: Math.max(40, 100 - missing * 20), color: '#34c759' },
    { label: '合规度', value: Math.max(30, 100 - risks * 15), color: risks > 2 ? '#f5a623' : '#34c759' },
    { label: '条款覆盖', value: Math.min(100, clauses * 15 + 30), color: '#0071e3' },
    { label: '格式规范', value: 90, color: '#af52de' },
  ]
})

function downloadDoc() {
  if (store.generateResult?.task_id) window.open('/api/export/' + store.generateResult.task_id, '_blank')
}

async function copyPreview() {
  try {
    await navigator.clipboard.writeText(store.generateResult?.preview || '')
    ElMessage.success('已复制到剪贴板')
  } catch { ElMessage.info('复制失败') }
}
</script>

<style scoped>
.step-head { text-align: center; margin-bottom: 24px; }
.success-icon { margin-bottom: 12px; }
.step-head h2 { font-size: 24px; font-weight: 650; letter-spacing: -0.5px; }
.step-head p { font-size: 14px; color: var(--text-secondary); margin-top: 4px; word-break: break-all; }
.section { margin-bottom: 24px; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.section-title { font-size: 15px; font-weight: 600; color: var(--text-primary); margin-bottom: 0; }
.copy-btn { font-size: 12px; padding: 5px 12px; }
.clause-card { padding: 14px 16px; border: 0.5px solid var(--border); border-radius: var(--radius-sm); margin-bottom: 8px; }
.clause-card h4 { font-size: 14px; font-weight: 550; color: var(--text-primary); margin-bottom: 4px; }
.clause-text { font-size: 13px; color: var(--text-secondary); line-height: 1.6; white-space: pre-wrap; }
.clause-reason { font-size: 12px; color: var(--accent); margin-top: 6px; }
.preview-box { white-space: pre-wrap; font-size: 13px; line-height: 1.8; color: var(--text-secondary); max-height: 360px; overflow-y: auto; background: rgba(128,128,128,0.04); padding: 16px; border-radius: var(--radius-sm); border: 0.5px solid var(--border); }
.step-actions { display: flex; justify-content: center; gap: 12px; margin-top: 28px; flex-wrap: wrap; }
.dl-btn { padding: 12px 28px; font-size: 15px; }
</style>
