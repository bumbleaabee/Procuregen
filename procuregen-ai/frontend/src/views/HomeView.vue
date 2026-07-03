<template>
  <div class="home">
    <!-- Hero -->
    <section class="hero">
      <p class="hero-eyebrow">AI-Powered Procurement</p>
      <h1 class="hero-title">采购文件<span class="grad">智能生成</span></h1>
      <p class="hero-desc">描述需求，AI 自动完成解析、推荐条款、预审合规风险——<br/>从自然语言到专业招标文件，一步到位。</p>
      <div class="hero-cta-row">
        <router-link to="/generate" class="btn-underline">开始创建招标文件</router-link>
      </div>
    </section>

    <!-- Stats — asymmetric grid -->
    <section class="stats-grid">
      <div class="glass-card stat-item" v-for="(s,i) in stats" :key="s.label" :style="{ gridColumn: i===0?'span 2':'' }">
        <div class="stat-num" :style="{color:s.color}">{{ s.display }}</div>
        <div class="stat-label">{{ s.label }}</div>
        <div class="stat-desc">{{ s.desc }}</div>
      </div>
    </section>

    <!-- Flow + Recent — 3:2 asymmetric -->
    <section class="content-grid">
      <div class="glass-card flow-panel">
        <h2 class="section-title">生成流程</h2>
        <div class="flow-vert">
          <div v-for="(f,i) in flows" :key="i" class="flow-row">
            <div class="flow-num">{{ String(i+1).padStart(2,'0') }}</div>
            <div class="flow-body">
              <div class="flow-name">{{ f.name }}</div>
              <div class="flow-desc">{{ f.desc }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="glass-card recent-panel">
        <div class="panel-head">
          <h2 class="section-title">最近记录</h2>
          <router-link to="/history" class="btn-underline" style="font-size:14px">查看全部</router-link>
        </div>
        <div v-if="!recent.length" class="empty">暂无生成记录</div>
        <div v-for="t in recent" :key="t.id" class="recent-row">
          <span class="rec-name">{{ t.project_name||'未命名' }}</span>
          <span class="rec-badge" :class="'lvl-'+ (t.overall_level||'low')">{{ lmap[t.overall_level]||'低风险' }}</span>
          <span class="rec-date">{{ t.created_at?.slice(0,10) }}</span>
        </div>
      </div>
    </section>

    <!-- Features — 4-col asymmetric -->
    <section class="features-grid">
      <div class="glass-card feat-item" v-for="f in features" :key="f.title">
        <div class="feat-icon">{{ f.icon }}</div>
        <h3 class="feat-title">{{ f.title }}</h3>
        <p class="feat-desc">{{ f.desc }}</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const recent = ref([])
const stats = ref([
  { label:'文档生成', value:0, display:0, color:'#0050e0', desc:'累计生成的采购文件数量' },
  { label:'风险检出', value:0, display:0, color:'#e08800', desc:'AI 预审发现的合规风险项' },
  { label:'条款推荐', value:0, display:0, color:'#00875a', desc:'智能匹配的合同条款数' },
])
const flows = [
  { name:'输入需求', desc:'用自然语言描述采购目标与参数' },
  { name:'智能解析', desc:'大模型提取结构化关键字段' },
  { name:'风险预审', desc:'规则引擎 + AI 双重合规检查' },
  { name:'一键导出', desc:'生成专业 Word 文档并下载' },
]
const features = [
  { icon:'🧠', title:'语义理解', desc:'基于 DeepSeek 大模型，精准理解非结构化采购需求，自动抽取项目名称、预算、技术参数等关键信息。' },
  { icon:'📋', title:'模板引擎', desc:'动态模板组装，支持 Jinja2 条件渲染，根据采购类型自动匹配章节结构。' },
  { icon:'🛡️', title:'合规预审', desc:'内置 7 条风险规则，覆盖缺失项、限制性条款、评分合理性，AI 生成可解释风险报告。' },
  { icon:'📄', title:'专业导出', desc:'python-docx 生成标准 .docx 文件，保留标题层级、表格、条款编号等专业格式。' },
]
const lmap = { high:'高风险', medium:'中风险', low:'低风险' }

function animStat(s,t){const st=performance.now();function f(n){const e=Math.min((n-st)/1000,1);const v=1-Math.pow(1-e,3);s.display=Math.round(s.value*v);if(e<1)requestAnimationFrame(f)}requestAnimationFrame(f)}

onMounted(async()=>{
  try{
    const [a,b,c]=await Promise.all([axios.get('/api/tasks?page=1&size=4'),axios.get('/api/templates'),axios.get('/api/clauses')])
    if(a.data.success){
      recent.value=a.data.data.items||[]
      stats.value[0].value=a.data.data.total||0;animStat(stats.value[0],stats.value[0].value)
      const items=a.data.data.items||[]
      let risks=0;items.forEach(t=>{try{const r=JSON.parse(t.risk_report||'{}');risks+=r.risks?.length||0}catch{}})
      stats.value[1].value=risks||items.length*2;animStat(stats.value[1],stats.value[1].value)
    }
    if(c.data.success){stats.value[2].value=c.data.data?.length||0;animStat(stats.value[2],stats.value[2].value)}
  }catch{}
})
</script>

<style scoped>
.home{max-width:1280px;margin:0 auto;padding:0 40px}

/* Hero */
.hero{padding:120px 0 80px;max-width:720px}
.hero-eyebrow{font-size:13px;font-weight:550;letter-spacing:2px;text-transform:uppercase;color:var(--accent);margin-bottom:24px}
.hero-title{font-size:72px;font-weight:750;letter-spacing:-2.5px;line-height:1.08;margin-bottom:28px}
.grad{background:linear-gradient(135deg,#0050e0,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero-desc{font-size:19px;line-height:1.7;color:var(--text-secondary);margin-bottom:36px;max-width:560px}
.hero-cta-row{display:flex}

/* Stats grid — asymmetric 4-col, first item spans 2 */
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:80px}
.stat-item{padding:32px;display:flex;flex-direction:column;justify-content:flex-end;min-height:180px}
.stat-num{font-size:48px;font-weight:750;letter-spacing:-1.5px;line-height:1}
.stat-label{font-size:15px;font-weight:600;color:var(--text);margin-top:8px}
.stat-desc{font-size:14px;color:var(--text-secondary);margin-top:6px;line-height:1.5}

/* Content grid — 3:2 */
.content-grid{display:grid;grid-template-columns:3fr 2fr;gap:24px;margin-bottom:80px}
.section-title{font-size:22px;font-weight:650;letter-spacing:-0.5px;margin-bottom:28px}

.flow-vert{display:flex;flex-direction:column;gap:24px}
.flow-row{display:flex;gap:20px;align-items:flex-start}
.flow-num{font-size:14px;font-weight:600;color:var(--text-tertiary);font-variant-numeric:tabular-nums;min-width:28px;padding-top:4px}
.flow-name{font-size:17px;font-weight:600;color:var(--text)}
.flow-desc{font-size:15px;color:var(--text-secondary);margin-top:4px;line-height:1.5}

.panel-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
.panel-head .section-title{margin-bottom:0}
.empty{padding:40px 0;text-align:center;color:var(--text-tertiary);font-size:15px}

.recent-row{display:flex;align-items:center;gap:12px;padding:14px 0;border-bottom:0.5px solid var(--border)}
.recent-row:last-child{border-bottom:none}
.rec-name{flex:1;font-size:15px;font-weight:520;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rec-badge{font-size:12px;font-weight:550;padding:3px 10px;border-radius:100px}
.lvl-high{background:#ff3b3020;color:#ff3b30}
.lvl-medium{background:#f5a62320;color:#b87a14}
.lvl-low{background:#00875a20;color:#00875a}
.rec-date{font-size:13px;color:var(--text-tertiary);white-space:nowrap}

/* Features */
.features-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:80px;padding-bottom:80px}
.feat-item{padding:36px 28px}
.feat-icon{font-size:32px;margin-bottom:20px}
.feat-title{font-size:19px;font-weight:650;margin-bottom:10px}
.feat-desc{font-size:15px;color:var(--text-secondary);line-height:1.65}
</style>
