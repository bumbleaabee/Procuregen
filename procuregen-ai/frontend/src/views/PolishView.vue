<template>
  <div class="polish-root">
    <div class="top">
      <h2>文档润色工作台</h2>
      <div class="actions-bar">
        <button v-for="a in actions" :key="a.key" class="act-btn" :class="{ on: mode === a.key }" @click="setMode(a.key)" :disabled="busy">
          <span class="act-icon">{{ a.icon }}</span>{{ a.label }}
        </button>
      </div>
    </div>

    <div class="panes">
      <div class="pane pane-left">
        <div class="pane-label">原始文本</div>
        <textarea v-model="input" class="pane-area" placeholder="在此粘贴或输入采购文档文本..."></textarea>
      </div>

      <div class="pane pane-right">
        <div class="pane-label">
          润色结果
          <button v-if="result && !busy" class="copy-btn" @click="copyResult">复制</button>
          <button v-if="result && !busy" class="apply-btn" @click="applyResult">← 应用</button>
        </div>
        <div class="pane-area result-area" :class="{ empty: !result && !busy }">
          <div v-if="busy" class="stream-text">{{ streamText }}<span class="cursor">|</span></div>
          <div v-else-if="result" class="stream-text">{{ result }}</div>
          <div v-else class="hint">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.3"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            <p>选择上方操作，AI 将在此显示结果</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const input = ref('')
const result = ref('')
const streamText = ref('')
const mode = ref('polish')
const busy = ref(false)
let ctrl = null

const actions = [
  { key: 'polish', label: '润色优化', icon: '✨' },
  { key: 'expand', label: '扩写补充', icon: '📝' },
  { key: 'shorten', label: '精简缩写', icon: '📋' },
  { key: 'formal', label: '正式化', icon: '🏛️' },
  { key: 'autocomplete', label: '智能续写', icon: '🤖' },
]

async function setMode(key) {
  mode.value = key
  await run()
}

async function run() {
  const t = input.value.trim()
  if (!t || busy.value) return
  busy.value = true; result.value = ''; streamText.value = ''
  if (ctrl) ctrl.abort(); ctrl = new AbortController()

  try {
    const u = `/api/polish-stream?text=${encodeURIComponent(t)}&action=${mode.value}`
    const r = await fetch(u, { signal: ctrl.signal })
    const reader = r.body.getReader(); const dec = new TextDecoder(); let buf = ''
    while (true) {
      const { done, value } = await reader.read(); if (done) break
      buf += dec.decode(value, { stream: true })
      const lines = buf.split('\n'); buf = lines.pop() || ''
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue
        try { const d = JSON.parse(line.slice(6)); if (d.done) { result.value = d.full; streamText.value = ''; busy.value = false; return } if (d.token) streamText.value += d.token } catch {}
      }
    }
  } catch { if (!result.value) result.value = streamText.value }
  busy.value = false
}

async function copyResult() { try { await navigator.clipboard.writeText(result.value) } catch {} }
function applyResult() { input.value = result.value; result.value = ''; streamText.value = '' }
</script>

<style scoped>
.polish-root { max-width: 960px; margin: 0 auto; }
.top { text-align: center; margin-bottom: 20px; }
.top h2 { font-size: 22px; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 14px; }
.actions-bar { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }
.act-btn {
  display: flex; align-items: center; gap: 6px; padding: 9px 18px;
  border-radius: 100px; border: 0.5px solid var(--border);
  background: var(--bg-glass); color: var(--text-secondary); font-size: 13px;
  cursor: pointer; transition: all var(--transition); font-family: var(--font); font-weight: 500;
}
.act-btn:hover:not(:disabled) { border-color: var(--accent); color: var(--accent); }
.act-btn.on { background: var(--accent); color: #fff; border-color: var(--accent); }
.act-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.act-icon { font-size: 15px; }

.panes { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; height: calc(100vh - 220px); }
.pane { display: flex; flex-direction: column; background: var(--bg-card); border-radius: var(--radius-lg); border: 0.5px solid var(--border); overflow: hidden; }
.pane-label { display: flex; align-items: center; gap: 8px; padding: 12px 16px; font-size: 12px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 0.5px solid var(--border); }
.copy-btn, .apply-btn { margin-left: auto; font-size: 11px; font-weight: 500; background: none; border: 0.5px solid var(--border); border-radius: 6px; padding: 3px 10px; cursor: pointer; color: var(--text-secondary); font-family: var(--font); transition: all var(--transition); }
.copy-btn:hover, .apply-btn:hover { border-color: var(--accent); color: var(--accent); }
.apply-btn { margin-left: 6px; }

.pane-area { flex: 1; padding: 16px; border: none; outline: none; resize: none; font-size: 14px; line-height: 1.75; font-family: var(--font); background: transparent; color: var(--text-primary); }
.pane-area::placeholder { color: var(--text-tertiary); }
.result-area { overflow-y: auto; }
.result-area.empty { display: flex; align-items: center; justify-content: center; }
.hint { text-align: center; color: var(--text-tertiary); }
.hint svg { margin-bottom: 12px; }
.hint p { font-size: 13px; }
.stream-text { white-space: pre-wrap; }
.cursor { color: var(--accent); font-weight: 100; animation: blink 1s step-end infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
</style>
