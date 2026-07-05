<template>
  <Teleport to="body">
    <Transition name="cmd">
      <div v-if="show" class="help-overlay" @click.self="$emit('close')">
        <div class="help-panel">
          <div class="help-header">
            <h3>键盘快捷键</h3>
            <button @click="$emit('close')" class="help-close">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            </button>
          </div>
          <div class="help-grid">
            <div v-for="s in shortcuts" :key="s.key" class="help-row">
              <kbd>{{ s.key }}</kbd>
              <span>{{ s.desc }}</span>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({ show: Boolean })
defineEmits(['close'])

const shortcuts = [
  { key: 'Ctrl+K', desc: '打开命令面板' },
  { key: '?', desc: '显示此帮助' },
  { key: 'Ctrl+D', desc: '切换暗色模式' },
  { key: 'Ctrl+N', desc: '新建采购文件' },
  { key: 'Ctrl+H', desc: '查看历史记录' },
  { key: 'Ctrl+T', desc: '模板管理' },
  { key: 'Esc', desc: '关闭弹窗/面板' },
]
</script>

<style scoped>
.help-overlay { position: fixed; inset: 0; z-index: 99999; background: rgba(0,0,0,0.4); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; }
.help-panel { width: 440px; background: var(--bg-card); backdrop-filter: blur(20px); border: 0.5px solid var(--border); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); padding: 24px; }
.help-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.help-header h3 { font-size: 17px; font-weight: 650; }
.help-close { background: none; border: none; cursor: pointer; color: var(--text-tertiary); padding: 4px; border-radius: 6px; }
.help-close:hover { background: var(--accent-ghost); color: var(--text); }
.help-grid { display: flex; flex-direction: column; gap: 8px; }
.help-row { display: flex; align-items: center; gap: 14px; padding: 8px 0; }
.help-row kbd { min-width: 80px; text-align: center; }
.help-row span { font-size: 14px; color: var(--text-secondary); }
</style>
