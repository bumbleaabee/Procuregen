<template>
  <div id="app-root" :class="{ 'sidebar-collapsed': isCollapse }">
    <!-- 侧边栏 — 毛玻璃效果 -->
    <aside class="sidebar">
      <div class="sidebar-inner">
        <router-link to="/" class="logo">
          <div class="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" stroke-width="1.5"/><line x1="8" y1="9" x2="16" y2="9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="13" x2="13" y2="13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          </div>
          <span v-show="!isCollapse" class="logo-text">ProcureGen</span>
        </router-link>

        <nav class="nav">
          <router-link to="/" class="nav-item" :class="{ active: route.path === '/' }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span v-show="!isCollapse">工作台</span>
          </router-link>
          <router-link to="/generate" class="nav-item" :class="{ active: route.path === '/generate' }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="8" x2="12" y2="16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="12" x2="16" y2="12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            <span v-show="!isCollapse">新建文件</span>
          </router-link>
          <router-link to="/history" class="nav-item" :class="{ active: route.path === '/history' }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/><polyline points="12 7 12 12 16 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span v-show="!isCollapse">历史记录</span>
          </router-link>
          <router-link to="/templates" class="nav-item" :class="{ active: route.path === '/templates' }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="14" y="3" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="3" y="14" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="14" y="14" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/></svg>
            <span v-show="!isCollapse">模板管理</span>
          </router-link>
          <router-link to="/chat" class="nav-item" :class="{ active: route.path === '/chat' }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2v10z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span v-show="!isCollapse">AI 顾问</span>
          </router-link>
          <router-link to="/analytics" class="nav-item" :class="{ active: route.path === '/analytics' }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="3" y="12" width="4" height="8" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="10" y="7" width="4" height="13" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="17" y="3" width="4" height="17" rx="1" stroke="currentColor" stroke-width="1.5"/></svg>
            <span v-show="!isCollapse">数据分析</span>
          </router-link>
          <router-link to="/knowledge" class="nav-item" :class="{ active: route.path === '/knowledge' }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M4 19.5A2.5 2.5 0 016.5 17H20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M4 5v14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M16 7H8M16 11H8M12 15H8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            <span v-show="!isCollapse">知识库</span>
          </router-link>
          <router-link to="/polish" class="nav-item" :class="{ active: route.path === '/polish' }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span v-show="!isCollapse">文档润色</span>
          </router-link>
          <router-link to="/guide" class="nav-item" :class="{ active: route.path === '/guide' }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><polygon points="12 2 22 8.5 12 15 2 8.5 12 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><polyline points="2 15 12 21 22 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span v-show="!isCollapse">流程导览</span>
          </router-link>
        </nav>

        <div class="sidebar-footer">
          <div class="status-dot" :class="{ connected: !mockMode }" />
          <span v-show="!isCollapse" class="status-text">{{ mockMode ? 'Mock' : 'DeepSeek AI' }}</span>
          <button class="theme-toggle" @click="toggleTheme" :title="isDark ? '切换亮色' : '切换暗色'">
            <svg v-if="!isDark" width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="1.5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          </button>
          <button class="collapse-btn" @click="isCollapse = !isCollapse">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" :style="{ transform: isCollapse ? 'rotate(180deg)' : '' }"><polyline points="15 18 9 12 15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- 主区域 -->
    <main class="main-area">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <LoadingOverlay :visible="isLoading" :status="loadStatus" />
    <KeyboardHelp :show="helpVisible" @close="helpVisible = false" />

    <!-- 粒子背景 -->
    <ParticleBackground />

    <!-- 命令面板 Ctrl+K -->
    <Teleport to="body">
      <Transition name="cmd">
        <div v-if="cmdVisible" class="cmd-overlay" @click.self="cmdVisible = false">
          <div class="cmd-panel">
            <div class="cmd-input-wrap">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="1.5"/><path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              <input ref="cmdInput" v-model="cmdQuery" class="cmd-input" placeholder="搜索命令..." @keydown.escape="cmdVisible = false" @keydown.enter="runFirstCmd" />
              <kbd>Esc</kbd>
            </div>
            <div class="cmd-list">
              <button v-for="(cmd, i) in filteredCmds" :key="i" class="cmd-item" @click="runCmd(cmd)">
                <span>{{ cmd.label }}</span>
                <kbd>{{ cmd.shortcut }}</kbd>
              </button>
              <div v-if="filteredCmds.length === 0" class="cmd-empty">无匹配命令</div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useTheme } from './composables/useTheme'
import { useGenerateStore } from './stores/generate'
import LoadingOverlay from './components/LoadingOverlay.vue'
import ParticleBackground from './components/ParticleBackground.vue'
import KeyboardHelp from './components/KeyboardHelp.vue'

const route = useRoute()
const router = useRouter()
const { isDark, toggle: toggleTheme } = useTheme()
const generateStore = useGenerateStore()
const isCollapse = ref(false)
const mockMode = ref(true)
const helpVisible = ref(false)

const isLoading = computed(() => generateStore.loading)
const loadStatus = computed(() => generateStore.loadingStatus)

// ── 命令面板 ──
const cmdVisible = ref(false)
const cmdQuery = ref('')
const cmdInput = ref(null)

const allCommands = [
  { label: '新建采购文件', shortcut: '⌘N', action: () => router.push('/generate') },
  { label: '查看历史记录', shortcut: '⌘H', action: () => router.push('/history') },
  { label: '模板管理', shortcut: '⌘T', action: () => router.push('/templates') },
  { label: '回到首页', shortcut: '⌘Home', action: () => router.push('/') },
  { label: '切换暗色模式', shortcut: '⌘D', action: () => toggleTheme() },
]

const filteredCmds = computed(() => {
  if (!cmdQuery.value) return allCommands
  const q = cmdQuery.value.toLowerCase()
  return allCommands.filter(c => c.label.toLowerCase().includes(q))
})

function runFirstCmd() {
  if (filteredCmds.value.length > 0) runCmd(filteredCmds.value[0])
}

function runCmd(cmd) {
  cmdVisible.value = false
  cmd.action()
}

// ── 键盘快捷键 ──
function onKeyDown(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); cmdVisible.value = true; nextTick(() => cmdInput.value?.focus()) }
  if (e.key === '?' && !e.ctrlKey && !e.metaKey && document.activeElement === document.body) { e.preventDefault(); helpVisible.value = !helpVisible.value }
  if (e.key === 'Escape') { helpVisible.value = false; cmdVisible.value = false }
}

onMounted(async () => {
  window.addEventListener('keydown', onKeyDown)
  // 自动暗色模式：18:00-06:00 自动切换
  if (!localStorage.getItem('theme')) {
    const hour = new Date().getHours()
    if (hour >= 18 || hour < 6) toggleTheme()
  }
  try {
    const root = await axios.get('/')
    mockMode.value = root.data?.llm?.is_mock ?? true
  } catch {}
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeyDown)
})
</script>

<style>
/* ═══════════════════════════════════════════
   Light Theme (default)
   ═══════════════════════════════════════════ */
:root {
  --bg-primary: #f5f5f7;
  --bg-card: rgba(255,255,255,0.72);
  --bg-card-hover: rgba(255,255,255,0.88);
  --bg-glass: rgba(255,255,255,0.64);
  --text-primary: #1d1d1f;
  --text-secondary: #86868b;
  --text-tertiary: #aeaeb2;
  --accent: #0071e3;
  --accent-hover: #0077ed;
  --accent-light: rgba(0,113,227,0.08);
  --border: rgba(0,0,0,0.06);
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.04), 0 2px 6px rgba(0,0,0,0.06);
  --shadow-lg: 0 12px 32px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04);
  --radius-sm: 10px;
  --radius: 16px;
  --radius-lg: 20px;
  --radius-xl: 24px;
  --transition: 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  --font: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* ═══════════════════════════════════════════
   Dark Theme
   ═══════════════════════════════════════════ */
.dark {
  --bg-primary: #0a0a0a;
  --bg-card: rgba(28,28,30,0.78);
  --bg-card-hover: rgba(44,44,46,0.85);
  --bg-glass: rgba(28,28,30,0.7);
  --text-primary: #f5f5f7;
  --text-secondary: #98989d;
  --text-tertiary: #636366;
  --accent: #0a84ff;
  --accent-hover: #409cff;
  --accent-light: rgba(10,132,255,0.12);
  --border: rgba(255,255,255,0.08);
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg: 0 12px 32px rgba(0,0,0,0.5);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: var(--font);
  background: var(--bg-primary);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow: hidden;
  transition: background var(--transition), color var(--transition);
}

#app-root { display: flex; height: 100vh; width: 100vw; position: relative; z-index: 1; }

/* ═══════════ Glow Effects ═══════════ */
.glow-blue { box-shadow: 0 0 30px rgba(0,113,227,0.15), 0 0 60px rgba(0,113,227,0.05); }
.glow-purple { box-shadow: 0 0 30px rgba(175,82,222,0.15), 0 0 60px rgba(175,82,222,0.05); }
.glow-green { box-shadow: 0 0 30px rgba(52,199,89,0.15), 0 0 60px rgba(52,199,89,0.05); }
.text-gradient {
  background: linear-gradient(135deg, #0071e3 0%, #af52de 50%, #ff6b6b 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.dark .text-gradient {
  background: linear-gradient(135deg, #0a84ff 0%, #bf5af2 50%, #ff6b6b 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ═══════════ Sidebar ═══════════ */
.sidebar { width: 220px; flex-shrink: 0; transition: width var(--transition); position: relative; z-index: 100; }
.sidebar-collapsed .sidebar { width: 68px; }
.sidebar-inner {
  position: fixed; top: 0; left: 0; width: 220px; height: 100vh;
  display: flex; flex-direction: column;
  background: var(--bg-glass);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-right: 0.5px solid var(--border);
  padding: 20px 12px;
  transition: all var(--transition);
  z-index: 200;
}
.sidebar-collapsed .sidebar-inner { width: 68px; }

.logo { display: flex; align-items: center; gap: 10px; padding: 8px 10px; text-decoration: none; color: var(--text-primary); margin-bottom: 32px; border-radius: var(--radius-sm); transition: background var(--transition); }
.logo:hover { background: var(--accent-light); }
.logo-icon { flex-shrink: 0; color: var(--accent); }
.logo-text { font-size: 17px; font-weight: 600; letter-spacing: -0.3px; white-space: nowrap; }

.nav { display: flex; flex-direction: column; gap: 2px; flex: 1; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 10px; text-decoration: none; color: var(--text-secondary); font-size: 14px; font-weight: 450; letter-spacing: -0.2px; border-radius: var(--radius-sm); transition: all var(--transition); white-space: nowrap; }
.nav-item:hover { background: var(--accent-light); color: var(--text-primary); }
.nav-item.active { background: var(--accent-light); color: var(--accent); font-weight: 540; }
.nav-item svg { flex-shrink: 0; }

.sidebar-footer { display: flex; align-items: center; gap: 8px; padding: 12px 10px; border-top: 0.5px solid var(--border); margin-top: auto; white-space: nowrap; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; background: #f5a623; flex-shrink: 0; transition: background var(--transition); }
.status-dot.connected { background: #34c759; }
.status-text { font-size: 12px; color: var(--text-tertiary); }
.theme-toggle { background: none; border: none; cursor: pointer; color: var(--text-tertiary); padding: 4px; border-radius: 6px; transition: all var(--transition); flex-shrink: 0; display: flex; align-items: center; }
.theme-toggle:hover { background: var(--accent-light); color: var(--accent); }
.collapse-btn { background: none; border: none; cursor: pointer; color: var(--text-tertiary); padding: 4px; border-radius: 6px; transition: all var(--transition); flex-shrink: 0; display: flex; align-items: center; }
.collapse-btn:hover { background: var(--accent-light); color: var(--text-primary); }

/* ═══════════ Main ═══════════ */
.main-area { flex: 1; overflow-y: auto; overflow-x: hidden; padding: 32px 40px; position: relative; z-index: 10; }

/* ═══════════ Command Palette ═══════════ */
.cmd-overlay { position: fixed; inset: 0; z-index: 9999; background: rgba(0,0,0,0.4); backdrop-filter: blur(4px); display: flex; justify-content: center; padding-top: 15vh; }
.dark .cmd-overlay { background: rgba(0,0,0,0.6); }
.cmd-panel { width: 560px; max-height: 420px; background: var(--bg-card); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 0.5px solid var(--border); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); overflow: hidden; }
.cmd-input-wrap { display: flex; align-items: center; gap: 10px; padding: 14px 16px; border-bottom: 0.5px solid var(--border); }
.cmd-input-wrap svg { color: var(--text-tertiary); flex-shrink: 0; }
.cmd-input { flex: 1; border: none; outline: none; font-size: 15px; font-family: var(--font); background: transparent; color: var(--text-primary); }
.cmd-input::placeholder { color: var(--text-tertiary); }
.cmd-list { max-height: 340px; overflow-y: auto; padding: 6px; }
.cmd-item { display: flex; align-items: center; justify-content: space-between; width: 100%; padding: 10px 14px; border: none; background: transparent; color: var(--text-primary); font-size: 14px; font-family: var(--font); cursor: pointer; border-radius: var(--radius-sm); transition: background var(--transition); text-align: left; }
.cmd-item:hover { background: var(--accent-light); }
kbd { font-size: 11px; padding: 2px 8px; border-radius: 4px; background: var(--accent-light); color: var(--text-secondary); font-family: var(--font); }
.cmd-empty { padding: 24px; text-align: center; color: var(--text-tertiary); font-size: 14px; }

.cmd-enter-active { transition: all 0.2s ease-out; }
.cmd-leave-active { transition: all 0.15s ease-in; }
.cmd-enter-from { opacity: 0; }
.cmd-enter-from .cmd-panel { transform: scale(0.96) translateY(-12px); }
.cmd-leave-to { opacity: 0; }
.cmd-leave-to .cmd-panel { transform: scale(0.96) translateY(-12px); }

/* ═══════════ Page Transition ═══════════ */
.page-enter-active { transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1); }
.page-leave-active { transition: all 0.2s cubic-bezier(0.4, 0, 0.6, 1); }
.page-enter-from { opacity: 0; transform: translateY(16px) scale(0.995); }
.page-leave-to { opacity: 0; transform: translateY(-8px) scale(0.998); }

/* ═══════════ Shared Apple Components ═══════════ */
.apple-card {
  background: var(--bg-card); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 0.5px solid var(--border); border-radius: var(--radius-lg);
  padding: 28px; box-shadow: var(--shadow-sm); transition: all var(--transition);
}
.apple-card:hover { box-shadow: var(--shadow-md); background: var(--bg-card-hover); }

.apple-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 10px 20px; font-family: var(--font); font-size: 14px; font-weight: 500;
  letter-spacing: -0.2px; border: none; border-radius: 100px; cursor: pointer;
  transition: all var(--transition); text-decoration: none;
}
.apple-btn-primary { background: var(--accent); color: #fff; }
.apple-btn-primary:hover { background: var(--accent-hover); box-shadow: 0 2px 8px rgba(0,113,227,0.3); transform: translateY(-1px); }
.apple-btn-primary:active { transform: scale(0.97); }
.apple-btn-secondary { background: var(--accent-light); color: var(--text-primary); }
.apple-btn-secondary:hover { background: rgba(128,128,128,0.12); }
.apple-btn:disabled { opacity: 0.4; cursor: not-allowed; pointer-events: none; }

.apple-input, .apple-textarea {
  width: 100%; padding: 12px 16px; font-family: var(--font); font-size: 15px;
  color: var(--text-primary); background: rgba(128,128,128,0.04);
  border: 0.5px solid var(--border); border-radius: var(--radius);
  outline: none; transition: all var(--transition); resize: vertical;
}
.apple-input:focus, .apple-textarea:focus {
  border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-light); background: var(--bg-card);
}
.apple-textarea { min-height: 160px; line-height: 1.6; }

/* ═══════════ Element Plus Overrides ═══════════ */
.el-card { border-radius: var(--radius-lg) !important; border: 0.5px solid var(--border) !important; box-shadow: var(--shadow-sm) !important; background: var(--bg-card) !important; color: var(--text-primary) !important; }
.el-button--primary { background: var(--accent) !important; border-color: var(--accent) !important; border-radius: 100px !important; font-weight: 500 !important; }
.el-button { border-radius: 100px !important; font-weight: 450 !important; transition: all var(--transition) !important; }
.el-tag { border-radius: 100px !important; font-weight: 500 !important; }
.el-table { border-radius: var(--radius-lg) !important; overflow: hidden; background: var(--bg-card) !important; color: var(--text-primary) !important; }
.el-table th { background: var(--accent-light) !important; font-weight: 500 !important; color: var(--text-secondary) !important; }
.el-table td { border-color: var(--border) !important; }
.el-dialog { border-radius: var(--radius-xl) !important; background: var(--bg-card) !important; }
.el-tabs__item { font-weight: 450 !important; color: var(--text-secondary) !important; }
.el-tabs__item.is-active { color: var(--accent) !important; }
.el-input__inner { background: transparent !important; color: var(--text-primary) !important; }
.el-select .el-input__inner { background: var(--bg-card) !important; }
.el-pagination button { background: transparent !important; color: var(--text-secondary) !important; }

/* ═══════════ Scrollbar ═══════════ */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(128,128,128,0.2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(128,128,128,0.35); }
</style>
