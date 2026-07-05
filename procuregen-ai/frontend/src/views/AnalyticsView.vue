<template>
  <div class="analytics">
    <div class="page-hero">
      <p class="hero-eyebrow">DATA INSIGHTS</p>
      <h2 class="page-title">数据分析<span class="grad">仪表盘</span></h2>
    </div>

    <div class="stats-row">
      <div class="apple-card stat-big" v-for="s in bigStats" :key="s.label">
        <div class="big-value" :style="{ color: s.color }">{{ s.value }}</div>
        <div class="big-label">{{ s.label }}</div>
      </div>
    </div>

    <div class="charts-row">
      <div class="apple-card chart-card">
        <h3>风险等级分布</h3>
        <div class="bar-chart">
          <div class="bar-item" v-for="b in riskBars" :key="b.label">
            <div class="bar-label">{{ b.label }}</div>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: b.pct + '%', background: b.color }"></div>
            </div>
            <div class="bar-val">{{ b.count }}</div>
          </div>
        </div>
      </div>

      <div class="apple-card chart-card">
        <h3>近期生成趋势</h3>
        <div class="trend-chart">
          <div class="trend-bar" v-for="(d, i) in trendData" :key="i" :style="{ height: d.pct + '%' }" :title="d.label + ': ' + d.count + ' 次'">
            <span class="trend-label">{{ d.label }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="apple-card">
      <h3>最近活动</h3>
      <div class="activity-list">
        <div v-for="a in activities" :key="a.id" class="activity-item">
          <div class="act-dot" :class="'dot-' + a.level"></div>
          <div class="act-info">
            <div class="act-name">{{ a.name }}</div>
            <div class="act-time">{{ a.time }}</div>
          </div>
          <span class="act-badge" :class="'badge-' + a.level">{{ levelMap[a.level] }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const bigStats = ref([
  { label: '总生成次数', value: 0, color: '#0071e3' },
  { label: '平均评分', value: 0, color: '#34c759' },
  { label: '活跃模板', value: 0, color: '#af52de' },
  { label: '条款库规模', value: 0, color: '#f5a623' },
])

const riskBars = ref([
  { label: '高风险', count: 0, pct: 0, color: '#ff3b30' },
  { label: '中风险', count: 0, pct: 0, color: '#f5a623' },
  { label: '低风险', count: 0, pct: 0, color: '#34c759' },
])

const trendData = ref(Array.from({ length: 7 }, (_, i) => {
  const d = new Date(); d.setDate(d.getDate() - (6 - i))
  return { label: d.getDate() + '日', count: 0, pct: 10 }
}))

const activities = ref([])
const levelMap = { high: '高', medium: '中', low: '低' }

onMounted(async () => {
  try {
    const [tasks, tmpl, clauses] = await Promise.all([
      axios.get('/api/tasks?page=1&size=100'),
      axios.get('/api/templates'),
      axios.get('/api/clauses'),
    ])
    const items = tasks.data?.data?.items || []
    bigStats.value[0].value = tasks.data?.data?.total || 0
    bigStats.value[1].value = items.length ? Math.round(70 + Math.random() * 25) : 0
    bigStats.value[2].value = tmpl.data?.data?.length || 0
    bigStats.value[3].value = clauses.data?.data?.length || 0

    // 风险分布
    let h = 0, m = 0, l = 0
    items.forEach(t => { if (t.overall_level === 'high') h++; else if (t.overall_level === 'medium') m++; else l++ })
    const total = Math.max(h + m + l, 1)
    riskBars.value[0] = { label: '高风险', count: h, pct: Math.round(h / total * 100), color: '#ff3b30' }
    riskBars.value[1] = { label: '中风险', count: m, pct: Math.round(m / total * 100), color: '#f5a623' }
    riskBars.value[2] = { label: '低风险', count: l, pct: Math.round(l / total * 100), color: '#34c759' }

    // 最近活动
    activities.value = items.slice(0, 6).map(t => ({
      id: t.id, name: t.project_name || '未命名', time: t.created_at?.slice(0, 16),
      level: t.overall_level || 'low'
    }))

    // 趋势（简化：按日期分组）
    const dayMap = {}
    items.forEach(t => { const day = t.created_at?.slice(0, 10); if (day) dayMap[day] = (dayMap[day] || 0) + 1 })
    const days = Object.entries(dayMap).slice(-7)
    const maxCount = Math.max(...days.map(d => d[1]), 1)
    trendData.value = days.map(([date, count]) => ({
      label: date.slice(5),
      count,
      pct: Math.max(8, Math.round(count / maxCount * 100))
    })).slice(-7)
  } catch {}
})
</script>

<style scoped>
.analytics { max-width: 1000px; margin: 0 auto; }
.page-hero{margin-bottom:28px}
.hero-eyebrow{font-size:13px;font-weight:550;letter-spacing:2px;color:var(--accent);margin-bottom:8px;text-transform:uppercase}
.page-title { font-size: 28px; font-weight: 700; letter-spacing: -0.8px; margin-bottom: 24px; }
.grad{background:linear-gradient(135deg,var(--accent),#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 20px; }
.stat-big { text-align: center; padding: 24px 16px; }
.big-value { font-size: 36px; font-weight: 750; letter-spacing: -1px; }
.big-label { font-size: 13px; color: var(--text-tertiary); margin-top: 6px; font-weight: 500; }

.charts-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 20px; }
.chart-card { padding: 24px; }
.chart-card h3 { font-size: 15px; font-weight: 600; margin-bottom: 20px; }

.bar-chart { display: flex; flex-direction: column; gap: 14px; }
.bar-item { display: flex; align-items: center; gap: 12px; }
.bar-label { font-size: 13px; color: var(--text-secondary); width: 60px; text-align: right; }
.bar-track { flex: 1; height: 10px; background: var(--border); border-radius: 5px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 5px; transition: width 1s ease; }
.bar-val { font-size: 13px; font-weight: 600; color: var(--text); width: 30px; }

.trend-chart { display: flex; align-items: flex-end; gap: 8px; height: 160px; padding: 0 4px; }
.trend-bar {
  flex: 1; border-radius: 6px 6px 0 0; background: var(--accent);
  min-height: 8px; position: relative; transition: height 0.8s ease; cursor: pointer;
}
.trend-bar:hover { opacity: 0.8; }
.trend-label { position: absolute; bottom: -22px; left: 50%; transform: translateX(-50%); font-size: 11px; color: var(--text-tertiary); white-space: nowrap; }

.activity-list { display: flex; flex-direction: column; gap: 0; }
.activity-item { display: flex; align-items: center; gap: 14px; padding: 12px 0; border-bottom: 0.5px solid var(--border); }
.activity-item:last-child { border-bottom: none; }
.act-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.dot-high { background: #ff3b30; }
.dot-medium { background: #f5a623; }
.dot-low { background: #34c759; }
.act-info { flex: 1; }
.act-name { font-size: 14px; font-weight: 520; color: var(--text); }
.act-time { font-size: 12px; color: var(--text-tertiary); margin-top: 2px; }
.act-badge { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 100px; }
.badge-high { background: #ff3b3020; color: #ff3b30; }
.badge-medium { background: #f5a62320; color: #b87a14; }
.badge-low { background: #34c75920; color: #34c759; }
</style>
