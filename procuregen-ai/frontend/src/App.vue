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
        </nav>

        <div class="sidebar-footer">
          <div class="status-dot" :class="{ connected: !mockMode }" />
          <span v-show="!isCollapse" class="status-text">{{ mockMode ? 'Mock' : 'DeepSeek AI' }}</span>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const isCollapse = ref(false)
const mockMode = ref(true)

onMounted(async () => {
  try {
    const root = await axios.get('/')
    mockMode.value = root.data?.llm?.is_mock ?? true
  } catch { /* keep default */ }
})
</script>

<style>
/* ═══════════════════════════════════════════
   Apple-style Global Design Tokens
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

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: var(--font);
  background: var(--bg-primary);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow: hidden;
}

#app-root {
  display: flex;
  height: 100vh;
  width: 100vw;
}

/* ═══════════════════════
   Sidebar — Frosted Glass
   ═══════════════════════ */
.sidebar {
  width: 220px;
  flex-shrink: 0;
  transition: width var(--transition);
  position: relative;
  z-index: 100;
}
.sidebar-collapsed .sidebar { width: 68px; }

.sidebar-inner {
  position: fixed;
  top: 0; left: 0;
  width: 220px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: rgba(255,255,255,0.72);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-right: 0.5px solid var(--border);
  padding: 20px 12px;
  transition: width var(--transition);
}
.sidebar-collapsed .sidebar-inner { width: 68px; }

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  text-decoration: none;
  color: var(--text-primary);
  margin-bottom: 32px;
  border-radius: var(--radius-sm);
  transition: background var(--transition);
}
.logo:hover { background: var(--accent-light); }
.logo-icon { flex-shrink: 0; color: var(--accent); }
.logo-text { font-size: 17px; font-weight: 600; letter-spacing: -0.3px; white-space: nowrap; }

.nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 450;
  letter-spacing: -0.2px;
  border-radius: var(--radius-sm);
  transition: all var(--transition);
  white-space: nowrap;
}
.nav-item:hover { background: rgba(0,0,0,0.04); color: var(--text-primary); }
.nav-item.active { background: var(--accent-light); color: var(--accent); font-weight: 540; }
.nav-item svg { flex-shrink: 0; }

.sidebar-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 10px;
  border-top: 0.5px solid var(--border);
  margin-top: auto;
  white-space: nowrap;
}
.status-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #f5a623;
  flex-shrink: 0;
  transition: background var(--transition);
}
.status-dot.connected { background: #34c759; }
.status-text { font-size: 12px; color: var(--text-tertiary); }
.collapse-btn {
  margin-left: auto;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-tertiary);
  padding: 4px;
  border-radius: 6px;
  transition: all var(--transition);
  flex-shrink: 0;
}
.collapse-btn:hover { background: rgba(0,0,0,0.06); color: var(--text-primary); }

/* ═══════════════════════
   Main Area
   ═══════════════════════ */
.main-area {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 32px 40px;
}

/* ═══════════════════════
   Page Transition
   ═══════════════════════ */
.page-enter-active { transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1); }
.page-leave-active { transition: all 0.2s cubic-bezier(0.4, 0, 0.6, 1); }
.page-enter-from { opacity: 0; transform: translateY(16px) scale(0.995); }
.page-leave-to { opacity: 0; transform: translateY(-8px) scale(0.998); }

/* ═══════════════════════
   Shared Apple-style Components
   ═══════════════════════ */
.apple-card {
  background: var(--bg-card);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 0.5px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 28px;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition);
}
.apple-card:hover {
  box-shadow: var(--shadow-md);
  background: var(--bg-card-hover);
}

.apple-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  font-family: var(--font);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: -0.2px;
  border: none;
  border-radius: 100px;
  cursor: pointer;
  transition: all var(--transition);
  text-decoration: none;
}
.apple-btn-primary {
  background: var(--accent);
  color: #fff;
}
.apple-btn-primary:hover { background: var(--accent-hover); box-shadow: 0 2px 8px rgba(0,113,227,0.3); }
.apple-btn-secondary {
  background: rgba(0,0,0,0.04);
  color: var(--text-primary);
}
.apple-btn-secondary:hover { background: rgba(0,0,0,0.08); }

.apple-input, .apple-textarea {
  width: 100%;
  padding: 12px 16px;
  font-family: var(--font);
  font-size: 15px;
  color: var(--text-primary);
  background: rgba(0,0,0,0.02);
  border: 0.5px solid var(--border);
  border-radius: var(--radius);
  outline: none;
  transition: all var(--transition);
  resize: vertical;
}
.apple-input:focus, .apple-textarea:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-light);
  background: #fff;
}
.apple-textarea { min-height: 160px; line-height: 1.6; }

/* Override Element Plus styles globally */
.el-card { border-radius: var(--radius-lg) !important; border: 0.5px solid var(--border) !important; box-shadow: var(--shadow-sm) !important; }
.el-button--primary { background: var(--accent) !important; border-color: var(--accent) !important; border-radius: 100px !important; font-weight: 500 !important; }
.el-button { border-radius: 100px !important; font-weight: 450 !important; transition: all var(--transition) !important; }
.el-tag { border-radius: 100px !important; font-weight: 500 !important; }
.el-steps { padding: 0 20px; }
.el-step__title { font-size: 14px !important; font-weight: 500 !important; }
.el-step__description { font-size: 12px !important; color: var(--text-tertiary) !important; }
.el-table { border-radius: var(--radius-lg) !important; overflow: hidden; }
.el-table th { background: rgba(0,0,0,0.02) !important; font-weight: 500 !important; color: var(--text-secondary) !important; }
.el-dialog { border-radius: var(--radius-xl) !important; }
.el-menu { border-right: none !important; }
.el-tabs__item { font-weight: 450 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.12); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.2); }
</style>
