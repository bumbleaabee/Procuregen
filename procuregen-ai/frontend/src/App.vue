<template>
  <div class="root" :class="{ dark: isDark, 'is-landing': isLanding }" @scroll.passive="onScroll" ref="rootRef">
    <!-- Navigation: transparent to solid on scroll -->
    <header class="nav" :class="{ scrolled: scrolled }">
      <div class="nav-inner">
        <router-link to="/" class="nav-brand" aria-label="首页">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="16" rx="2.2" stroke="currentColor" stroke-width="1.5"/><line x1="8" y1="10" x2="16" y2="10" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/><line x1="8" y1="14" x2="13" y2="14" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
        </router-link>

        <nav class="nav-menu">
          <router-link v-for="n in mainNav" :key="n.to" :to="n.to" class="nav-link" :class="{ active: $route.path === n.to }">{{ n.label }}</router-link>
        </nav>

        <div class="nav-actions">
          <button class="nav-icon-btn" @click="toggleTheme" :aria-label="isDark?'亮色模式':'暗色模式'">
            <svg v-if="isDark" width="17" height="17" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="1.5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            <svg v-else width="17" height="17" viewBox="0 0 24 24" fill="none"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          </button>
          <router-link to="/generate" class="nav-cta">开始创建</router-link>
        </div>
      </div>
    </header>

    <main class="main">
      <router-view v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </router-view>
    </main>

    <LoadingOverlay :visible="busy" :status="sts" />

    <!-- 命令面板 -->
    <Teleport to="body"><Transition name="cm"><div v-if="cmd" class="cmd-bg" @click.self="cmd=false"><div class="cmd-box"><div class="cmd-h"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="1.5"/><path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg><input ref="ci" v-model="cq" class="cmd-in" placeholder="Search commands..." @keydown.escape="cmd=false" @keydown.enter="goC"/></div><div class="cmd-l"><button v-for="(c,i) in fc" :key="i" class="cmd-it" @click="doC(c)"><span>{{c.label}}</span><kbd>{{c.key}}</kbd></button></div></div></div></Transition></Teleport>
    <KeyboardHelp :show="hlp" @close="hlp=false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTheme } from './composables/useTheme'
import { useGenerateStore } from './stores/generate'
import LoadingOverlay from './components/LoadingOverlay.vue'
import KeyboardHelp from './components/KeyboardHelp.vue'

const route = useRoute()
const router = useRouter()
const { isDark, toggle: toggleTheme } = useTheme()
const gs = useGenerateStore()
const busy = computed(() => gs.loading)
const sts = computed(() => gs.loadingStatus)
const scrolled = ref(false)
const rootRef = ref(null)

const isLanding = computed(() => route.path === '/')

const mainNav = [
  { to:'/', label:'工作台' },
  { to:'/generate', label:'新建文件' },
  { to:'/chat', label:'AI 顾问' },
  { to:'/polish', label:'文档润色' },
  { to:'/analytics', label:'数据分析' },
  { to:'/knowledge', label:'知识库' },
  { to:'/guide', label:'流程导览' },
  { to:'/history', label:'历史记录' },
]

function onScroll() { scrolled.value = (rootRef.value?.scrollTop || 0) > 20 }

const cmd=ref(false),cq=ref(''),ci=ref(null),hlp=ref(false)
const all=[
  {label:'新建采购文件',key:'Ctrl+N',action:()=>router.push('/generate')},
  {label:'AI 顾问',key:'Ctrl+1',action:()=>router.push('/chat')},
  {label:'文档润色',key:'Ctrl+2',action:()=>router.push('/polish')},
  {label:'数据分析',key:'Ctrl+3',action:()=>router.push('/analytics')},
  {label:'知识库',key:'Ctrl+4',action:()=>router.push('/knowledge')},
  {label:'流程导览',key:'Ctrl+5',action:()=>router.push('/guide')},
  {label:'历史记录',key:'Ctrl+H',action:()=>router.push('/history')},
  {label:'模板管理',key:'Ctrl+T',action:()=>router.push('/templates')},
  {label:'切换主题',key:'Ctrl+D',action:()=>toggleTheme()},
]
const fc=computed(()=>cq.value?all.filter(c=>c.label.includes(cq.value)):all)
function goC(){if(fc.value[0])doC(fc.value[0])}
function doC(c){cmd.value=false;c.action()}

function onKey(e){
  if((e.metaKey||e.ctrlKey)&&e.key==='k'){e.preventDefault();cmd.value=true;nextTick(()=>ci.value?.focus())}
  if(e.key==='?'&&document.activeElement===document.body){e.preventDefault();hlp.value=!hlp.value}
  if(e.key==='Escape'){cmd.value=false;hlp.value=false}
}

onMounted(()=>{window.addEventListener('keydown',onKey)})
onUnmounted(()=>window.removeEventListener('keydown',onKey))
</script>

<style>
/* ══════════════════════════════════════
   Design System �?Content-First
   Typography | Space | Light | Motion
   ══════════════════════════════════════ */
:root {
  --bg: #fafaf9;
  --bg-elevated: rgba(255,255,255,0.72);
  --bg-glass: rgba(255,255,255,0.55);
  --text: #1a1a1a;
  --text-secondary: #5c5c5c;
  --text-tertiary: #999;
  --accent: #0050e0;
  --accent-hover: #003db0;
  --accent-ghost: rgba(0,80,224,0.06);
  --border: rgba(0,0,0,0.06);
  --border-glass: rgba(0,0,0,0.04);
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.03), 0 1px 3px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.04), 0 2px 6px rgba(0,0,0,0.03);
  --shadow-lg: 0 12px 40px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.03);
  --radius: 16px;
  --radius-sm: 10px;
  --ease: cubic-bezier(0.22,1,0.36,1);
  --font: "Inter", -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Microsoft YaHei", sans-serif;
}
.dark {
  --bg: #0a0a0a;
  --bg-elevated: rgba(20,20,20,0.75);
  --bg-glass: rgba(20,20,20,0.58);
  --text: #ededed;
  --text-secondary: #888;
  --text-tertiary: #555;
  --accent: #2b8aff;
  --accent-hover: #409cff;
  --accent-ghost: rgba(43,138,255,0.08);
  --border: rgba(255,255,255,0.06);
  --border-glass: rgba(255,255,255,0.04);
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.2);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.3);
  --shadow-lg: 0 12px 40px rgba(0,0,0,0.4);
}

*{margin:0;padding:0;box-sizing:border-box}
html{font-family:var(--font);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;overflow-y:scroll}
body{background:var(--bg);color:var(--text);overflow:hidden}
body::before{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.5;
  background:
    radial-gradient(ellipse 80% 50% at 20% 10%,rgba(43,138,255,.06),transparent),
    radial-gradient(ellipse 60% 40% at 80% 80%,rgba(124,58,237,.04),transparent),
    radial-gradient(ellipse 50% 50% at 50% 50%,rgba(43,138,255,.03),transparent);
  animation:bgShift 15s ease-in-out infinite alternate;
}
@keyframes bgShift{0%{opacity:.4;transform:scale(1)}50%{opacity:.6;transform:scale(1.05)}100%{opacity:.4;transform:scale(1)}}
body::after{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.03'/%3E%3C/svg%3E");
  opacity:.4;
}
.root{display:flex;flex-direction:column;height:100vh;overflow-y:auto;overflow-x:hidden;position:relative;z-index:1;scrollbar-gutter:stable;scroll-behavior:smooth}

/* ── Navigation ── */
.nav{position:sticky;top:0;z-index:100;transition:all 0.4s var(--ease)}
.nav.hidden{opacity:0;pointer-events:none}
.nav-inner{
  display:flex;align-items:center;max-width:1440px;margin:0 auto;
  padding:16px 40px;gap:48px;
}
.nav.scrolled .nav-inner{
  background:var(--bg-glass);backdrop-filter:blur(28px) saturate(200%);
  -webkit-backdrop-filter:blur(28px) saturate(200%);
  border-bottom:0.5px solid var(--border-glass);
  box-shadow:0 1px 0 rgba(0,0,0,0.03);
}
.nav.scrolled::after{
  content:'';position:absolute;bottom:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--accent),var(--accent-ghost),transparent);
  opacity:0;transition:opacity .5s var(--ease);
}
.nav.scrolled:hover::after{opacity:.6}

.nav-brand{display:flex;align-items:center;color:var(--text);text-decoration:none;flex-shrink:0}
.nav-menu{display:flex;align-items:center;gap:4px;flex:1;justify-content:center}
.nav-link{
  padding:8px 18px;border-radius:100px;text-decoration:none;
  color:var(--text-secondary);font-size:15px;font-weight:450;
  letter-spacing:-0.1px;transition:all 0.25s var(--ease);
  position:relative;
}
.nav-link::after{
  content:'';position:absolute;bottom:4px;left:50%;transform:translateX(-50%);
  width:0;height:2px;background:var(--accent);border-radius:1px;
  transition:width 0.25s var(--ease);
}
.nav-link:hover{background:var(--accent-ghost);color:var(--text)}
.nav-link.active{color:var(--text)}
.nav-link.active::after{width:18px}
.nav-actions{display:flex;align-items:center;gap:12px;flex-shrink:0;margin-left:auto}
.nav-icon-btn{
  background:none;border:none;color:var(--text-secondary);cursor:pointer;
  padding:8px;border-radius:100px;transition:all .25s var(--ease);display:flex;
}
.nav-icon-btn:hover{background:var(--accent-ghost);color:var(--text);transform:scale(1.08)}
.nav-icon-btn:active{transform:scale(.94)}
.nav-cta{
  padding:9px 24px;border-radius:100px;background:var(--accent);color:#fff;
  text-decoration:none;font-size:14px;font-weight:550;letter-spacing:-.2px;
  transition:all .25s var(--ease);
}
.nav-cta:hover{background:var(--accent-hover);transform:translateY(-1px);box-shadow:0 4px 20px rgba(0,80,224,.25)}
.nav-cta:active{transform:scale(.96)}

/* ── Main ── */
.main{flex:1}

/* ── Page transitions ── */
.page-enter-active{transition:all 0.35s var(--ease)}
.page-leave-active{transition:all 0.2s var(--ease)}
.page-enter-from{opacity:0;transform:translateY(12px)}
.page-leave-to{opacity:0;transform:translateY(-8px)}


/* ── Shared primitives ── */
.glass-card{
  background:var(--bg-elevated);backdrop-filter:blur(28px) saturate(200%);
  -webkit-backdrop-filter:blur(28px) saturate(200%);
  border:0.5px solid var(--border-glass);border-radius:var(--radius);
  box-shadow:0 1px 0 rgba(255,255,255,.05) inset,0 2px 8px rgba(0,0,0,.04),0 8px 32px rgba(0,0,0,.05);
  transition:all .45s var(--ease);
  position:relative;overflow:hidden;
}
.dark .glass-card{box-shadow:0 1px 0 rgba(255,255,255,.02) inset,0 2px 8px rgba(0,0,0,.3),0 8px 32px rgba(0,0,0,.4)}
.glass-card::before{
  content:'';position:absolute;inset:0;border-radius:inherit;
  background:radial-gradient(ellipse at 50% 0%,rgba(43,138,255,.08),transparent 70%);
  opacity:0;transition:opacity .5s var(--ease);z-index:0;pointer-events:none;
}
.glass-card::after{
  content:'';position:absolute;top:0;left:-100%;width:60%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.04),transparent);
  transform:skewX(-20deg);transition:left .8s var(--ease);z-index:0;pointer-events:none;
}
.glass-card:hover::before{opacity:1}
.glass-card:hover::after{left:120%}
.glass-card:hover{
  box-shadow:0 1px 0 rgba(255,255,255,.08) inset,0 4px 16px rgba(0,0,0,.06),0 12px 40px rgba(0,0,0,.08);
  transform:translateY(-3px);
}

.surface-card{background:var(--bg);border-radius:var(--radius);padding:32px}

.btn-primary{
  display:inline-flex;align-items:center;gap:8px;padding:14px 32px;
  border-radius:100px;background:var(--accent);color:#fff;
  font-size:16px;font-weight:550;letter-spacing:-0.2px;
  border:none;cursor:pointer;font-family:inherit;
  transition:all 0.3s var(--ease);text-decoration:none;
}
.btn-primary:hover{background:var(--accent-hover);transform:translateY(-1px);box-shadow:0 8px 24px rgba(0,80,224,0.2)}
.btn-primary:active{transform:scale(0.96)}
.btn-primary:active{transform:scale(0.97)}
.btn-primary:disabled{opacity:0.3;pointer-events:none}

.btn-ghost{
  display:inline-flex;align-items:center;gap:8px;padding:14px 32px;
  border-radius:100px;background:transparent;color:var(--text);
  font-size:16px;font-weight:480;letter-spacing:-0.2px;
  border:0.5px solid var(--border);cursor:pointer;font-family:inherit;
  transition:all 0.3s var(--ease);text-decoration:none;
}
.btn-ghost:hover{border-color:var(--text-secondary);background:var(--accent-ghost)}

.btn-underline{
  display:inline-flex;align-items:center;gap:8px;
  padding:4px 0;background:none;border:none;
  color:var(--accent);font-size:16px;font-weight:520;
  cursor:pointer;font-family:inherit;
  border-bottom:1.5px solid var(--accent);
  transition:all 0.3s var(--ease);text-decoration:none;
}
.btn-underline:hover{border-bottom-width:2.5px;gap:14px}

/* Fade-in on scroll */
.fade-up{opacity:0;transform:translateY(24px);transition:all 0.6s var(--ease)}
.fade-up.visible{opacity:1;transform:translateY(0)}

/* Compat aliases */
.apple-card,.card{background:var(--bg-elevated);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:0.5px solid var(--border-glass);border-radius:var(--radius);padding:32px;box-shadow:var(--shadow-sm)}
.apple-btn,.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 24px;border-radius:100px;font-size:15px;font-weight:500;border:none;cursor:pointer;font-family:inherit;transition:all 0.3s var(--ease);text-decoration:none}
.apple-btn-primary,.btn-p{background:var(--accent);color:#fff}
.apple-btn-secondary,.btn-s{background:var(--accent-ghost);color:var(--text)}
.apple-btn:disabled,.btn:disabled{opacity:0.3;pointer-events:none}
.apple-input,.input{width:100%;padding:14px 18px;border-radius:var(--radius-sm);border:0.5px solid var(--border);background:var(--bg);color:var(--text);font-size:16px;font-family:inherit;outline:none;transition:all 0.3s var(--ease)}
.apple-input:focus,.input:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-ghost)}
.apple-textarea,.textarea{width:100%;padding:14px 18px;border-radius:var(--radius-sm);border:0.5px solid var(--border);background:var(--bg);color:var(--text);font-size:16px;font-family:inherit;outline:none;resize:vertical;min-height:140px;line-height:1.7;transition:all 0.3s var(--ease)}
.apple-textarea:focus,.textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-ghost)}

/* CMD palette */
.cmd-bg{position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,0.25);backdrop-filter:blur(6px);display:flex;justify-content:center;padding-top:16vh}
.cmd-box{width:480px;background:var(--bg-elevated);backdrop-filter:blur(32px);border:0.5px solid var(--border-glass);border-radius:var(--radius);box-shadow:var(--shadow-lg);overflow:hidden}
.cmd-h{display:flex;align-items:center;gap:12px;padding:16px 18px;border-bottom:0.5px solid var(--border);color:var(--text-tertiary)}
.cmd-in{flex:1;border:none;outline:none;font-size:16px;background:transparent;color:var(--text);font-family:inherit}
.cmd-in::placeholder{color:var(--text-tertiary)}
.cmd-l{max-height:300px;overflow-y:auto;padding:6px}
.cmd-it{display:flex;align-items:center;justify-content:space-between;width:100%;padding:10px 14px;border:none;background:transparent;color:var(--text);font-size:15px;cursor:pointer;border-radius:var(--radius-sm);font-family:inherit;text-align:left;transition:background 0.15s}
.cmd-it:hover{background:var(--accent-ghost)}
kbd{font-size:12px;padding:3px 8px;border-radius:6px;background:var(--accent-ghost);color:var(--text-tertiary);font-family:inherit;font-weight:500}
.cm-enter-active{transition:all 0.15s ease-out}.cm-leave-active{transition:all 0.1s ease-in}
.cm-enter-from{opacity:0}.cm-enter-from .cmd-box{transform:scale(0.96)}.cm-leave-to{opacity:0}

/* Element Plus overrides */
.el-card{border-radius:var(--radius)!important;border:0.5px solid var(--border-glass)!important;background:var(--bg-elevated)!important;color:var(--text)!important;box-shadow:none!important}
.el-button--primary{background:var(--accent)!important;border-color:var(--accent)!important;border-radius:100px!important;font-weight:520!important}
.el-button{border-radius:100px!important;font-weight:480!important}
.el-table{background:transparent!important;color:var(--text)!important;border-radius:var(--radius)!important;--el-table-bg-color:transparent!important;--el-table-tr-bg-color:transparent!important;--el-table-header-bg-color:var(--accent-ghost)!important}
.el-table th{background:var(--accent-ghost)!important;color:var(--text-secondary)!important;border-color:var(--border)!important;font-weight:550!important}
.el-table td{background:transparent!important;border-color:var(--border)!important;color:var(--text)!important}
.el-table__body tr:hover>td{background:var(--accent-ghost)!important}
.el-table--striped .el-table__body tr.el-table__row--striped td{background:var(--bg3)!important}
.el-dialog{background:var(--bg-elevated)!important;border-radius:var(--radius)!important;backdrop-filter:blur(20px)!important}
.el-input__inner{background:transparent!important;color:var(--text)!important;font-size:16px!important}
.el-input__wrapper{background:var(--bg)!important;box-shadow:none!important;border:0.5px solid var(--border)!important}
.el-tabs__item{font-size:15px!important;color:var(--text-secondary)!important}.el-tabs__item.is-active{color:var(--accent)!important}
.el-pagination button{background:transparent!important;color:var(--text-secondary)!important}
.el-pagination button:disabled{color:var(--text-tertiary)!important}
.el-tag{background:var(--accent-ghost)!important;border-color:transparent!important;color:var(--accent)!important}
.el-select .el-input__wrapper{background:var(--bg)!important}
.el-popper{background:var(--bg-elevated)!important;border:0.5px solid var(--border)!important;backdrop-filter:blur(20px)!important}
.el-select-dropdown__item{color:var(--text)!important}
.el-select-dropdown__item.hover,.el-select-dropdown__item:hover{background:var(--accent-ghost)!important}

::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
</style>
