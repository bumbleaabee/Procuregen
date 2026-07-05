<template>
  <div class="landing">
    <!-- Hero -->
    <section class="hero-sec">
      <div class="hero-bg"><div class="mesh"></div><div class="dots"></div>
        <div class="floating-orbs">
          <div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div>
          <div class="orb o4"></div><div class="orb o5"></div>
        </div>
      </div>
      <div class="hero-sec-bottom-mask"></div>
      <div class="hero-content">
        <div class="hero-logo"><svg width="48" height="48" viewBox="0 0 56 56" fill="none"><rect x="8" y="10" width="40" height="36" rx="7" stroke="currentColor" stroke-width="2.2"/><line x1="19" y1="23" x2="37" y2="23" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="19" y1="30" x2="31" y2="30" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></div>
        <h1 class="hero-name">ProcureGen</h1>
        <p class="hero-tagline">AI 驱动的采购文件智能生成系统<span>语义理解 · 模板引擎 · 风险预审 · 一键导出</span></p>
        <button class="hero-enter" @click="scrollDown">探索功能</button>
      </div>
    </section>

    <!-- Content -->
    <section ref="homeRef" class="home-sec">
      <div class="home-inner">
        <!-- Stats -->
        <div class="stats-grid">
          <div class="glass-card stat-item st1" v-for="(s,i) in stats" :key="s.label" :style="{ gridColumn: i===0?'span 2':'' }">
            <div class="stat-num" :style="{color:s.color}">{{ s.display }}</div>
            <div class="stat-label">{{ s.label }}</div>
            <div class="stat-desc">{{ s.desc }}</div>
          </div>
        </div>

        <div class="intro-block st2">
          <p class="intro-eyebrow">HOW IT WORKS</p>
          <h2 class="intro-title">从需求到文档<span class="grad">四步完成</span></h2>
        </div>

        <div class="flow-row">
          <div class="glass-card flow-item st3" v-for="(f,i) in flows" :key="i" :style="{ transitionDelay: i*0.1+'s' }">
            <div class="flow-num">{{ String(i+1).padStart(2,'0') }}</div>
            <h3 class="flow-name">{{ f.name }}</h3>
            <p class="flow-desc">{{ f.desc }}</p>
          </div>
        </div>

        <div class="cta-block st4">
          <h2>准备好开始了吗？</h2>
          <p>描述采购需求，AI 自动完成文档生成。</p>
          <router-link to="/generate" class="btn-primary">开始创建招标文件</router-link>
        </div>

        <div class="feat-grid">
          <div class="glass-card feat-card st5" v-for="(f,i) in features" :key="f.title" :style="{ transitionDelay: i*0.1+'s' }">
            <div class="feat-icon">{{ f.icon }}</div>
            <h3>{{ f.title }}</h3>
            <p>{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const homeRef = ref(null)
const stats = ref([
  { label:'累计生成', value:0, display:0, color:'#2b8aff', desc:'采购文件生成总量' },
  { label:'风险检出', value:0, display:0, color:'#e08800', desc:'AI 预审发现的风险项' },
  { label:'条款推荐', value:0, display:0, color:'#00875a', desc:'智能匹配的合同条款' },
])
const flows = [
  { name:'输入需求', desc:'用自然语言描述采购目标与参数' },
  { name:'AI 智能解析', desc:'DeepSeek 大模型提取结构化字段' },
  { name:'合规风险预审', desc:'规则引擎 + AI 双重合规检查' },
  { name:'一键导出文档', desc:'生成专业 .docx 文件并下载' },
]
const features = [
  { icon:'Brain', title:'语义理解', desc:'基于 DeepSeek 的 NLP 引擎精准提取项目名称、预算、技术参数等关键信息。' },
  { icon:'Layout', title:'模板引擎', desc:'Jinja2 动态模板组装，支持条件渲染与条款智能匹配。' },
  { icon:'Shield', title:'合规预审', desc:'内置 7 条风险规则，覆盖缺失项、限制性条款与评分合理性。' },
  { icon:'FileDown', title:'专业导出', desc:'python-docx 生成标准 .docx 文件，保留标题层级与表格格式。' },
]

function animStat(s,t){const st=performance.now();function f(n){const e=Math.min((n-st)/1000,1);const v=1-Math.pow(1-e,3);s.display=Math.round(s.value*v);if(e<1)requestAnimationFrame(f)}requestAnimationFrame(f)}

function scrollDown(){homeRef.value?.scrollIntoView({behavior:'smooth'})}

// Scroll reveal observer
let observer
onMounted(async()=>{
  observer = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');observer.unobserve(e.target)}})
  },{threshold:0.12,rootMargin:'0px 0px -40px 0px'})
  document.querySelectorAll('.st1,.st2,.st3,.st4,.st5').forEach(el=>observer.observe(el))

  try{
    const [a,c]=await Promise.all([axios.get('/api/tasks?page=1&size=4'),axios.get('/api/clauses')])
    if(a.data.success){stats.value[0].value=a.data.data.total||0;animStat(stats.value[0],stats.value[0].value);const items=a.data.data.items||[];let risks=0;items.forEach(t=>{try{const r=JSON.parse(t.risk_report||'{}');risks+=r.risks?.length||0}catch{}});stats.value[1].value=risks||items.length*2;animStat(stats.value[1],stats.value[1].value)}
    if(c.data.success){stats.value[2].value=c.data.data?.length||0;animStat(stats.value[2],stats.value[2].value)}
  }catch{}
})
onUnmounted(()=>observer?.disconnect())
</script>

<style scoped>
.landing{overflow-x:hidden}

/* Hero */
.hero-sec{position:relative;min-height:100vh;display:flex;align-items:center;justify-content:center;overflow:hidden}
.hero-sec::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse 60% 50% at 50% 40%,rgba(43,138,255,.04),transparent);
  animation:heroGlow 8s ease-in-out infinite alternate;
}
@keyframes heroGlow{0%{opacity:.6;transform:scale(1)}100%{opacity:1;transform:scale(1.15)}}
.hero-sec::after{
  content:'';position:absolute;width:600px;height:600px;border-radius:50%;
  background:radial-gradient(circle,rgba(124,58,237,.06),transparent 70%);
  top:50%;left:50%;transform:translate(-50%,-50%);
  animation:heroOrb 12s ease-in-out infinite;
  pointer-events:none;
}
@keyframes heroOrb{0%,100%{transform:translate(-50%,-50%) scale(1)}50%{transform:translate(-40%,-60%) scale(1.2)}}
.hero-bg{position:absolute;inset:0}
.mesh{position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 30% 20%,rgba(43,138,255,.1),transparent),radial-gradient(ellipse 60% 70% at 70% 70%,rgba(175,82,222,.07),transparent)}
.dots{position:absolute;inset:0;background-image:radial-gradient(circle,rgba(255,255,255,.03) 1px,transparent 1px);background-size:32px 32px}

/* Floating orbs */
.floating-orbs{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.orb{position:absolute;border-radius:50%;filter:blur(60px);animation:orbFloat 8s ease-in-out infinite}
.o1{width:300px;height:300px;background:rgba(43,138,255,.12);top:10%;left:15%;animation-delay:0s}
.o2{width:200px;height:200px;background:rgba(124,58,237,.1);top:60%;left:70%;animation-delay:-3s}
.o3{width:250px;height:250px;background:rgba(43,138,255,.08);top:40%;left:40%;animation-delay:-5s}
.o4{width:180px;height:180px;background:rgba(175,82,222,.07);top:5%;left:80%;animation-delay:-7s}
.o5{width:220px;height:220px;background:rgba(43,138,255,.06);top:70%;left:5%;animation-delay:-2s}
@keyframes orbFloat{0%,100%{transform:translateY(0) scale(1)}33%{transform:translateY(-30px) scale(1.15)}66%{transform:translateY(20px) scale(.95)}}
.hero-content{position:relative;z-index:1;text-align:center;padding:0 24px}
.hero-logo{color:#2b8aff;margin-bottom:20px;animation:heroLogoIn .9s cubic-bezier(.16,1,.3,1) both}
@keyframes heroLogoIn{from{opacity:0;transform:scale(.8) translateY(20px)}to{opacity:1;transform:scale(1) translateY(0)}}
.hero-name{font-size:56px;font-weight:800;letter-spacing:-2.5px;color:var(--text);margin-bottom:12px;animation:heroFadeUp .8s .15s cubic-bezier(.16,1,.3,1) both;text-shadow:0 0 80px rgba(43,138,255,.15)}
@keyframes heroFadeUp{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)}}
.hero-tagline{font-size:17px;color:var(--text-secondary);animation:heroFadeUp .8s .3s cubic-bezier(.16,1,.3,1) both}
.hero-tagline span{display:block;font-size:13px;color:var(--text-tertiary);margin-top:6px;letter-spacing:1.5px}
.hero-enter{margin-top:40px;padding:16px 36px;border-radius:100px;border:1px solid var(--border);background:transparent;color:var(--text);font-size:15px;font-weight:520;cursor:pointer;font-family:inherit;transition:all .35s var(--ease);animation:heroFadeUp .8s .5s cubic-bezier(.16,1,.3,1) both}
.hero-enter:hover{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 8px 28px rgba(43,138,255,.25);transform:translateY(-2px)}

/* Fog transition mask */
.hero-sec-bottom-mask{position:absolute;bottom:0;left:0;right:0;height:200px;background:linear-gradient(to bottom,transparent,var(--bg));pointer-events:none;z-index:2}

/* Home content */
.home-sec{padding:80px 0 120px}
.home-inner{max-width:1280px;margin:0 auto;padding:0 40px}

/* Stats */
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:80px}
.stat-item{padding:32px;display:flex;flex-direction:column;justify-content:flex-end;min-height:180px}
.stat-num{font-size:48px;font-weight:750;letter-spacing:-1.5px;line-height:1}
.stat-label{font-size:16px;font-weight:600;color:var(--text);margin-top:8px}
.stat-desc{font-size:14px;color:var(--text-secondary);margin-top:6px;line-height:1.5}

.intro-block{max-width:600px;margin-bottom:48px}
.intro-eyebrow{font-size:13px;font-weight:550;letter-spacing:2px;color:var(--accent);margin-bottom:16px}
.intro-title{font-size:40px;font-weight:700;letter-spacing:-1px;line-height:1.2}
.grad{background:linear-gradient(135deg,#2b8aff,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent}

.flow-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:80px}
.flow-item{padding:32px 24px}
.flow-num{font-size:14px;font-weight:600;color:var(--text-tertiary);margin-bottom:16px}
.flow-name{font-size:18px;font-weight:650;margin-bottom:8px}
.flow-desc{font-size:15px;color:var(--text-secondary);line-height:1.6}

.cta-block{text-align:center;padding:80px 0;border-top:0.5px solid var(--border);border-bottom:0.5px solid var(--border);margin-bottom:80px}
.cta-block h2{font-size:36px;font-weight:700;letter-spacing:-1px;margin-bottom:12px}
.cta-block p{font-size:17px;color:var(--text-secondary);margin-bottom:32px}

.feat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.feat-card{padding:36px 28px}
.feat-icon{font-size:32px;margin-bottom:20px}
.feat-card h3{font-size:19px;font-weight:650;margin-bottom:10px}
.feat-card p{font-size:15px;color:var(--text-secondary);line-height:1.65}

/* Scroll reveal */
.st1,.st2,.st3,.st4,.st5{opacity:0;transform:translateY(32px);transition:all .7s cubic-bezier(.16,1,.3,1)}
.st1.visible,.st2.visible,.st3.visible,.st4.visible,.st5.visible{opacity:1;transform:translateY(0)}
</style>
