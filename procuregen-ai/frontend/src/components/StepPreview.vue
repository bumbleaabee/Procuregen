<template>
  <div class="step">
    <div class="step-head">
      <div class="success-icon">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="11" fill="#34c75920" stroke="#34c759" stroke-width="1.5"/><polyline points="7 12 10.5 15.5 17 9" stroke="#34c759" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <h2>文档生成完成</h2>
      <p>文件：{{ store.generateResult?.file_name || '' }}</p>
    </div>

    <div v-if="store.selectedClauses?.length" class="section">
      <h3 class="section-title">推荐合同条款</h3>
      <div v-for="(clause, idx) in store.selectedClauses" :key="idx" class="clause-card">
        <h4>{{ clause.title }}</h4>
        <p class="clause-text">{{ clause.content?.slice(0, 200) }}{{ clause.content?.length > 200 ? '...' : '' }}</p>
        <p class="clause-reason">{{ clause.reason }}</p>
      </div>
    </div>

    <div class="section">
      <h3 class="section-title">文档预览</h3>
      <div class="preview-box">{{ store.generateResult?.preview || '暂无预览' }}</div>
    </div>

    <div class="step-actions">
      <button class="apple-btn apple-btn-secondary" @click="store.reset()">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="8" x2="12" y2="16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="12" x2="16" y2="12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
        新建文件
      </button>
      <button class="apple-btn apple-btn-primary" @click="downloadDoc" style="padding:12px 28px;font-size:15px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><polyline points="7 10 12 15 17 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><line x1="12" y1="15" x2="12" y2="3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
        下载 Word 文档
      </button>
      <router-link to="/history" class="apple-btn apple-btn-secondary">历史记录</router-link>
    </div>
  </div>
</template>

<script setup>
import { useGenerateStore } from '../stores/generate'
const store = useGenerateStore()
function downloadDoc() {
  if (store.generateResult?.task_id) window.open(`/api/export/${store.generateResult.task_id}`, '_blank')
}
</script>

<style scoped>
.step-head { text-align: center; margin-bottom: 32px; }
.success-icon { margin-bottom: 12px; }
.step-head h2 { font-size: 24px; font-weight: 650; letter-spacing: -0.5px; }
.step-head p { font-size: 14px; color: var(--text-secondary); margin-top: 4px; word-break: break-all; }
.section { margin-bottom: 24px; }
.section-title { font-size: 15px; font-weight: 600; margin-bottom: 12px; color: var(--text-primary); }
.clause-card { padding: 14px 16px; border: 0.5px solid var(--border); border-radius: var(--radius-sm); margin-bottom: 8px; }
.clause-card h4 { font-size: 14px; font-weight: 550; color: var(--text-primary); margin-bottom: 4px; }
.clause-text { font-size: 13px; color: var(--text-secondary); line-height: 1.6; white-space: pre-wrap; }
.clause-reason { font-size: 12px; color: var(--accent); margin-top: 6px; }
.preview-box { white-space: pre-wrap; font-size: 13px; line-height: 1.8; color: var(--text-secondary); max-height: 360px; overflow-y: auto; background: rgba(0,0,0,0.015); padding: 16px; border-radius: var(--radius-sm); border: 0.5px solid var(--border); }
.step-actions { display: flex; justify-content: center; gap: 12px; margin-top: 28px; flex-wrap: wrap; }
</style>
