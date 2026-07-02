<template>
  <div class="home">
    <!-- Hero 区域 -->
    <section class="hero">
      <h1 class="hero-title">采购文件<span class="accent">智能生成</span></h1>
      <p class="hero-sub">输入自然语言需求，AI 自动解析参数、推荐条款、预审风险，<br/>一键导出专业招标文件。</p>
      <div class="hero-actions">
        <router-link to="/generate" class="apple-btn apple-btn-primary" style="padding:12px 28px;font-size:15px;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="8" x2="12" y2="16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="12" x2="16" y2="12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          新建采购文件
        </router-link>
        <router-link to="/history" class="apple-btn apple-btn-secondary" style="padding:12px 24px;font-size:15px;">
          查看历史
        </router-link>
      </div>
    </section>

    <!-- 统计卡片 -->
    <section class="stats">
      <div class="stat-card" v-for="s in stats" :key="s.label">
        <div class="stat-icon" :style="{ color: s.color }">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" v-html="s.icon"></svg>
        </div>
        <div class="stat-value">{{ s.value }}</div>
        <div class="stat-label">{{ s.label }}</div>
      </div>
    </section>

    <!-- 流程 + 最近记录 -->
    <section class="bottom-row">
      <div class="apple-card flow-card">
        <h3 class="card-title">生成流程</h3>
        <div class="flow-steps">
          <div class="flow-step done">
            <div class="flow-num">1</div>
            <div class="flow-text">
              <div class="flow-name">输入需求</div>
              <div class="flow-desc">自然语言描述</div>
            </div>
          </div>
          <div class="flow-line"></div>
          <div class="flow-step done">
            <div class="flow-num">2</div>
            <div class="flow-text">
              <div class="flow-name">智能解析</div>
              <div class="flow-desc">AI 提取参数</div>
            </div>
          </div>
          <div class="flow-line"></div>
          <div class="flow-step done">
            <div class="flow-num">3</div>
            <div class="flow-text">
              <div class="flow-name">风险预审</div>
              <div class="flow-desc">合规检查</div>
            </div>
          </div>
          <div class="flow-line"></div>
          <div class="flow-step done">
            <div class="flow-num">4</div>
            <div class="flow-text">
              <div class="flow-name">一键导出</div>
              <div class="flow-desc">下载 Word</div>
            </div>
          </div>
        </div>
      </div>

      <div class="apple-card recent-card">
        <div class="card-header">
          <h3 class="card-title">最近记录</h3>
          <router-link to="/history" class="link">查看全部</router-link>
        </div>
        <div v-if="recentTasks.length === 0" class="empty">
          <div class="empty-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" stroke-width="1.2"/></svg>
          </div>
          <p>暂无生成记录</p>
          <router-link to="/generate" class="apple-btn apple-btn-primary" style="font-size:13px;padding:8px 16px;margin-top:8px;">立即创建</router-link>
        </div>
        <div v-else>
          <div v-for="task in recentTasks" :key="task.id" class="recent-item">
            <div class="recent-info">
              <div class="recent-name">{{ task.project_name || '未命名项目' }}</div>
              <div class="recent-meta">
                <span class="recent-badge" :class="'badge-' + (task.overall_level || 'low')">{{ levelMap[task.overall_level] || '低' }}</span>
                <span class="recent-time">{{ task.created_at?.slice(0, 10) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 能力 -->
    <section class="capabilities">
      <div class="cap-item" v-for="c in capabilities" :key="c">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><polyline points="20 6 9 17 4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <span>{{ c }}</span>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const recentTasks = ref([])
const stats = ref([
  { label: '总生成', value: 0, color: '#0071e3', icon: '<rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" stroke-width="1.5"/><line x1="8" y1="9" x2="16" y2="9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="13" x2="13" y2="13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>' },
  { label: '模板', value: 0, color: '#34c759', icon: '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><polyline points="14 2 14 8 20 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>' },
  { label: '条款', value: 0, color: '#f5a623', icon: '<path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><rect x="9" y="3" width="6" height="4" rx="1" stroke="currentColor" stroke-width="1.5"/>' },
  { label: '规则', value: 7, color: '#ff3b30', icon: '<path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><line x1="12" y1="9" x2="12" y2="13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><circle cx="12" cy="17" r="0.5" fill="currentColor" stroke="none"/>' },
])
const levelMap = { high: '高', medium: '中', low: '低' }
const capabilities = ['自然语言需求解析', '结构化参数提取', '合同条款智能推荐', '合规风险自动预审', 'Word 文档一键导出', '历史记录可追溯']

onMounted(async () => {
  try {
    const [tasks, tmpl, clauses] = await Promise.all([
      axios.get('/api/tasks?page=1&size=4'),
      axios.get('/api/templates'),
      axios.get('/api/clauses'),
    ])
    if (tasks.data.success) {
      recentTasks.value = tasks.data.data.items || []
      stats.value[0].value = tasks.data.data.total || 0
    }
    if (tmpl.data.success) stats.value[1].value = tmpl.data.data?.length || 0
    if (clauses.data.success) stats.value[2].value = clauses.data.data?.length || 0
  } catch {}
})
</script>

<style scoped>
.home { max-width: 960px; margin: 0 auto; }
.hero { text-align: center; padding: 48px 0 40px; }
.hero-title { font-size: 44px; font-weight: 700; letter-spacing: -1.2px; color: var(--text-primary); line-height: 1.15; }
.hero-title .accent { background: linear-gradient(135deg, #0071e3, #42a5f5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { font-size: 17px; color: var(--text-secondary); line-height: 1.6; margin: 16px 0 28px; letter-spacing: -0.2px; }
.hero-actions { display: flex; gap: 12px; justify-content: center; }

/* Stats */
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 32px; }
.stat-card {
  background: var(--bg-card); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 0.5px solid var(--border); border-radius: var(--radius-lg); padding: 22px 20px;
  text-align: center; transition: all var(--transition); cursor: default;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
.stat-icon { margin-bottom: 10px; display: flex; justify-content: center; }
.stat-value { font-size: 32px; font-weight: 700; letter-spacing: -0.5px; color: var(--text-primary); }
.stat-label { font-size: 13px; color: var(--text-tertiary); margin-top: 4px; font-weight: 450; }

/* Bottom */
.bottom-row { display: grid; grid-template-columns: 1.2fr 1fr; gap: 16px; margin-bottom: 28px; }
.card-title { font-size: 17px; font-weight: 600; letter-spacing: -0.3px; margin-bottom: 16px; }

/* Flow */
.flow-steps { display: flex; align-items: flex-start; gap: 0; }
.flow-step { display: flex; align-items: flex-start; gap: 10px; flex: 1; min-width: 0; }
.flow-num {
  width: 28px; height: 28px; border-radius: 50%; background: var(--accent-light); color: var(--accent);
  display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600; flex-shrink: 0;
}
.flow-name { font-size: 14px; font-weight: 550; color: var(--text-primary); }
.flow-desc { font-size: 12px; color: var(--text-tertiary); margin-top: 2px; }
.flow-line { width: 20px; height: 1px; background: var(--border); margin: 13px 2px 0; flex-shrink: 0; }

/* Recent */
.recent-card { min-height: 200px; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.card-header .card-title { margin-bottom: 0; }
.link { font-size: 13px; color: var(--accent); text-decoration: none; font-weight: 500; }
.link:hover { text-decoration: underline; }
.empty { text-align: center; padding: 24px 0; color: var(--text-tertiary); }
.empty-icon { margin-bottom: 8px; color: var(--text-tertiary); }
.empty p { font-size: 14px; margin-bottom: 0; }
.recent-item { padding: 12px 0; border-bottom: 0.5px solid var(--border); transition: background var(--transition); }
.recent-item:last-child { border-bottom: none; }
.recent-name { font-size: 14px; font-weight: 520; color: var(--text-primary); margin-bottom: 4px; }
.recent-meta { display: flex; align-items: center; gap: 8px; }
.recent-badge {
  font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 100px;
  background: #34c75920; color: #34c759;
}
.badge-high { background: #ff3b3020; color: #ff3b30; }
.badge-medium { background: #f5a62320; color: #f5a623; }
.badge-low { background: #34c75920; color: #34c759; }
.recent-time { font-size: 12px; color: var(--text-tertiary); }

/* Capabilities */
.capabilities { display: flex; flex-wrap: wrap; gap: 6px 20px; justify-content: center; }
.cap-item {
  display: flex; align-items: center; gap: 6px;
  font-size: 13px; color: var(--text-secondary); padding: 6px 0;
}
.cap-item svg { color: #34c759; flex-shrink: 0; }
</style>
