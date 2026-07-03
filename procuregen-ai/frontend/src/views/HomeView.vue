<template>
  <div class="home">
    <div class="floating-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>

    <section class="hero">
      <div class="hero-badge">
        <span class="badge-dot"></span> Powered by DeepSeek AI
      </div>
      <h1 class="hero-title">
        <span class="title-line">采购文件</span>
        <span class="title-line text-gradient">智能生成系统</span>
      </h1>
      <p class="hero-sub">输入自然语言需求，AI 自动解析参数、推荐条款、预审风险<br/>一键导出专业招标文件</p>
      <div class="hero-actions">
        <router-link to="/generate" class="apple-btn apple-btn-primary hero-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="8" x2="12" y2="16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="12" x2="16" y2="12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          开始创建
        </router-link>
        <router-link to="/history" class="apple-btn apple-btn-secondary hero-btn">查看历史 →</router-link>
      </div>
    </section>

    <section class="stats">
      <div class="stat-card glow-blue" v-for="s in stats" :key="s.label">
        <div class="stat-icon" :style="{ color: s.color }"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" v-html="s.icon"></svg></div>
        <div class="stat-value">{{ s.display }}</div>
        <div class="stat-label">{{ s.label }}</div>
      </div>
    </section>

    <section class="bottom-row">
      <div class="apple-card flow-card">
        <h3 class="card-title">⚡ 四步生成</h3>
        <div class="flow-steps">
          <div class="flow-step" v-for="(f, i) in flows" :key="i">
            <div class="flow-num">{{ i + 1 }}</div>
            <div class="flow-text"><div class="flow-name">{{ f.name }}</div><div class="flow-desc">{{ f.desc }}</div></div>
            <div v-if="i < 3" class="flow-arrow"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><polyline points="9 18 15 12 9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div>
          </div>
        </div>
      </div>

      <div class="apple-card recent-card">
        <div class="card-header"><h3 class="card-title">📋 最近记录</h3><router-link to="/history" class="link">全部 →</router-link></div>
        <div v-if="!recentTasks.length" class="empty-state"><p>还没有生成记录</p><router-link to="/generate" class="apple-btn apple-btn-primary" style="font-size:13px;padding:8px 16px;margin-top:12px;">创建第一个</router-link></div>
        <div v-else>
          <div v-for="task in recentTasks" :key="task.id" class="recent-item">
            <div class="recent-name">{{ task.project_name || '未命名' }}</div>
            <div class="recent-meta">
              <span class="recent-badge" :class="'badge-' + (task.overall_level || 'low')">{{ levelMap[task.overall_level] || '低' }}</span>
              <span class="recent-time">{{ task.created_at?.slice(0, 10) }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const recentTasks = ref([])
const stats = ref([
  { label: '总生成', value: 0, display: 0, color: '#0071e3', icon: '<rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" stroke-width="1.5"/><line x1="8" y1="9" x2="16" y2="9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="13" x2="13" y2="13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>' },
  { label: '模板', value: 0, display: 0, color: '#34c759', icon: '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><polyline points="14 2 14 8 20 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>' },
  { label: '条款', value: 0, display: 0, color: '#f5a623', icon: '<path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><rect x="9" y="3" width="6" height="4" rx="1" stroke="currentColor" stroke-width="1.5"/>' },
  { label: '规则', value: 7, display: 7, color: '#ff3b30', icon: '<path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><line x1="12" y1="9" x2="12" y2="13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><circle cx="12" cy="17" r="0.5" fill="currentColor" stroke="none"/>' },
])
const levelMap = { high: '高', medium: '中', low: '低' }
const flows = [
  { name: '输入需求', desc: '自然语言描述' },
  { name: '智能解析', desc: 'AI 提取参数' },
  { name: '风险预审', desc: '合规检查' },
  { name: '一键导出', desc: '下载 Word' },
]

function animateValue(stat, target) {
  const start = stat.display; const duration = 800; const startTime = performance.now()
  function step(now) { const elapsed = now - startTime; const progress = Math.min(elapsed / duration, 1); const eased = 1 - Math.pow(1 - progress, 3); stat.display = Math.round(start + (target - start) * eased); if (progress < 1) requestAnimationFrame(step) }
  requestAnimationFrame(step)
}

onMounted(async () => {
  try {
    const [tasks, tmpl, clauses] = await Promise.all([axios.get('/api/tasks?page=1&size=4'), axios.get('/api/templates'), axios.get('/api/clauses')])
    if (tasks.data.success) { recentTasks.value = tasks.data.data.items || []; animateValue(stats.value[0], tasks.data.data.total || 0) }
    if (tmpl.data.success) animateValue(stats.value[1], tmpl.data.data?.length || 0)
    if (clauses.data.success) animateValue(stats.value[2], clauses.data.data?.length || 0)
  } catch {}
})
</script>

<style scoped>
.home { max-width: 1000px; margin: 0 auto; position: relative; }
.floating-shapes { position: absolute; inset: 0; pointer-events: none; overflow: hidden; z-index: 0; }
.shape { position: absolute; border-radius: 50%; opacity: 0.06; animation: floatShape 20s ease-in-out infinite; }
.shape-1 { width: 300px; height: 300px; background: var(--accent); top: 5%; right: -10%; filter: blur(40px); }
.shape-2 { width: 200px; height: 200px; background: #af52de; top: 40%; left: -8%; animation-delay: -7s; filter: blur(30px); }
.shape-3 { width: 250px; height: 250px; background: #34c759; bottom: 10%; right: 20%; animation-delay: -14s; filter: blur(35px); }
@keyframes floatShape { 0%,100% { transform: translate(0,0) rotate(0deg) scale(1); } 33% { transform: translate(30px,-20px) rotate(120deg) scale(1.1); } 66% { transform: translate(-20px,15px) rotate(240deg) scale(0.9); } }

.hero { text-align: center; padding: 56px 0 44px; position: relative; z-index: 1; }
.hero-badge { display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; border-radius: 100px; background: var(--accent-light); border: 0.5px solid var(--border); font-size: 13px; font-weight: 500; color: var(--text-secondary); margin-bottom: 24px; backdrop-filter: blur(8px); }
.badge-dot { width: 7px; height: 7px; border-radius: 50%; background: #34c759; animation: pulse 2s ease-in-out infinite; }
.hero-title { font-size: 52px; font-weight: 750; letter-spacing: -1.5px; line-height: 1.2; margin-bottom: 20px; }
.title-line { display: block; }
.text-gradient { background: linear-gradient(135deg, #0071e3 0%, #af52de 50%, #ff6b6b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { font-size: 17px; color: var(--text-secondary); line-height: 1.7; margin-bottom: 32px; }
.hero-actions { display: flex; gap: 12px; justify-content: center; }
.hero-btn { padding: 13px 28px; font-size: 15px; }

.stats { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 36px; position: relative; z-index: 1; }
.stat-card { background: var(--bg-card); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 0.5px solid var(--border); border-radius: var(--radius-lg); padding: 24px 20px; text-align: center; transition: all 0.4s cubic-bezier(0.23,1,0.32,1); cursor: default; }
.stat-card:hover { transform: translateY(-4px); }
.stat-icon { margin-bottom: 10px; display: flex; justify-content: center; }
.stat-value { font-size: 34px; font-weight: 750; letter-spacing: -0.5px; color: var(--text-primary); }
.stat-label { font-size: 13px; color: var(--text-tertiary); margin-top: 4px; font-weight: 500; }

.bottom-row { display: grid; grid-template-columns: 1.2fr 1fr; gap: 16px; margin-bottom: 24px; position: relative; z-index: 1; }
.card-title { font-size: 17px; font-weight: 650; letter-spacing: -0.3px; margin-bottom: 16px; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.card-header .card-title { margin-bottom: 0; }
.link { font-size: 13px; color: var(--accent); text-decoration: none; font-weight: 550; }
.link:hover { text-decoration: underline; }

.flow-steps { display: flex; align-items: center; gap: 0; }
.flow-step { display: flex; align-items: center; gap: 10px; flex: 1; }
.flow-num { width: 30px; height: 30px; border-radius: 50%; background: var(--accent-light); color: var(--accent); display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 650; flex-shrink: 0; }
.flow-name { font-size: 14px; font-weight: 550; color: var(--text-primary); white-space: nowrap; }
.flow-desc { font-size: 12px; color: var(--text-tertiary); }
.flow-arrow { color: var(--text-tertiary); flex-shrink: 0; opacity: 0.4; }

.recent-card { min-height: 180px; }
.empty-state { text-align: center; padding: 28px 0; }
.empty-state p { color: var(--text-tertiary); font-size: 14px; }
.recent-item { padding: 12px 0; border-bottom: 0.5px solid var(--border); }
.recent-item:last-child { border-bottom: none; }
.recent-name { font-size: 14px; font-weight: 520; color: var(--text-primary); margin-bottom: 4px; }
.recent-meta { display: flex; align-items: center; gap: 8px; }
.recent-badge { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 100px; }
.badge-high { background: #ff3b3020; color: #ff3b30; }
.badge-medium { background: #f5a62320; color: #b87a14; }
.badge-low { background: #34c75920; color: #34c759; }
.recent-time { font-size: 12px; color: var(--text-tertiary); }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }
</style>
