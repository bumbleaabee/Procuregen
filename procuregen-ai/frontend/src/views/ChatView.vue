<template>
  <div class="chat-root">
    <div class="chat-main">
      <!-- 消息列表 -->
      <div class="msg-list" ref="listRef">
        <div v-if="msgs.length === 0" class="empty">
          <div class="empty-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2v10z"/></svg>
          </div>
          <h3>采购智能顾问</h3>
          <p>基于 DeepSeek，精通采购法规与实务</p>
          <div class="quick-row">
            <button v-for="q in quicks" :key="q" class="quick" @click="ask(q)">{{ q }}</button>
          </div>
        </div>

        <template v-for="(m, i) in msgs" :key="i">
          <div class="msg" :class="m.role">
            <div class="msg-avatar">{{ m.role === 'user' ? 'U' : 'AI' }}</div>
            <div class="msg-bubble">
              <div class="msg-text" v-if="m.content" v-html="m.html"></div>
              <span v-if="m.streaming && !m.content" class="think-dots"><i>●</i><i>●</i><i>●</i></span>
              <span v-if="m.streaming && m.content" class="cursor">|</span>
            </div>
          </div>
        </template>

        <div ref="anchorRef"></div>
      </div>

      <!-- 输入栏 -->
      <div class="bar">
        <div class="bar-inner">
          <input
            ref="inputRef"
            v-model="text"
            class="bar-input"
            placeholder="输入问题，Enter 发送"
            @keydown.enter="send"
            :disabled="busy"
          />
          <button class="bar-btn" :class="{ on: text.trim() && !busy }" :disabled="!text.trim() || busy" @click="send">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const msgs = ref([])
const text = ref('')
const busy = ref(false)
const listRef = ref(null)
const anchorRef = ref(null)
const inputRef = ref(null)
let ctrl = null

const quicks = [
  '公开招标的完整流程？',
  '招标文件必备章节？',
  '评分标准怎么设计？',
  '违约责任条款怎么写？',
  '履约保证金比例？',
  '信息化采购特殊要求？',
]

function html(s) {
  return s
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/\n\n/g, '<br><br>')
    .replace(/\n/g, '<br>')
}

async function ask(q) {
  text.value = q
  await nextTick()
  send()
}

async function send() {
  const t = text.value.trim()
  if (!t || busy.value) return
  text.value = ''
  busy.value = true

  msgs.value.push({ role: 'user', content: t, html: html(t) })
  const ai = { role: 'assistant', content: '', html: '', streaming: true }
  msgs.value.push(ai)
  scroll()

  if (ctrl) ctrl.abort()
  ctrl = new AbortController()

  try {
    const u = `/api/chat-stream?message=${encodeURIComponent(t)}`
    const r = await fetch(u, { signal: ctrl.signal })
    const reader = r.body.getReader()
    const dec = new TextDecoder()
    let buf = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buf += dec.decode(value, { stream: true })
      const lines = buf.split('\n')
      buf = lines.pop() || ''
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue
        try {
          const d = JSON.parse(line.slice(6))
          if (d.done) { ai.streaming = false; busy.value = false; ai.html = html(ai.content); scroll(); return }
          if (d.token) { ai.content += d.token; ai.html = html(ai.content); scroll() }
        } catch {}
      }
    }
  } catch {
    if (!ai.content) { ai.content = '(请求失败)'; ai.html = html(ai.content) }
  }
  ai.streaming = false
  busy.value = false
  ai.html = html(ai.content)
  scroll()
}

function scroll() {
  nextTick(() => {
    anchorRef.value?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  })
}
</script>

<style scoped>
.chat-root { height: calc(100vh - 72px); display: flex; flex-direction: column; }
.chat-main { flex: 1; display: flex; flex-direction: column; max-width: 780px; margin: 0 auto; width: 100%; background: var(--bg-card); border-radius: var(--radius-lg); border: 0.5px solid var(--border); overflow: hidden; }

/* ── Messages ── */
.msg-list { flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 20px; }
.empty { text-align: center; padding: 52px 0 36px; }
.empty-icon { color: var(--accent); opacity: 0.5; margin-bottom: 16px; }
.empty h3 { font-size: 18px; font-weight: 650; margin-bottom: 4px; }
.empty p { font-size: 13px; color: var(--text-secondary); margin-bottom: 24px; }
.quick-row { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; max-width: 500px; margin: 0 auto; }
.quick {
  padding: 8px 16px; border-radius: 100px; border: 0.5px solid var(--border);
  background: var(--bg-glass); color: var(--text-secondary); font-size: 13px;
  cursor: pointer; transition: all var(--transition); font-family: var(--font);
}
.quick:hover { border-color: var(--accent); color: var(--accent); background: var(--accent-light); }

/* ── Message bubble ── */
.msg { display: flex; gap: 10px; }
.msg.user { flex-direction: row-reverse; }
.msg-avatar {
  width: 30px; height: 30px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 700; letter-spacing: -0.2px; margin-top: 2px;
}
.msg.user .msg-avatar { background: var(--accent); color: #fff; }
.msg.assistant .msg-avatar { background: #34c759; color: #fff; }

.msg-bubble {
  max-width: 72%; padding: 10px 16px; border-radius: 18px;
  font-size: 14px; line-height: 1.65;
}
.msg.user .msg-bubble { background: var(--accent); color: #fff; border-bottom-right-radius: 6px; }
.msg.assistant .msg-bubble { background: rgba(128,128,128,0.06); color: var(--text-primary); border-bottom-left-radius: 6px; }

.msg-text :deep(b) { font-weight: 650; }
.msg.user .msg-text :deep(b) { color: #fff; }

/* ── Cursor ── */
.cursor {
  display: inline; font-weight: 100; color: var(--accent);
  animation: blink 1s step-end infinite; margin-left: 1px;
}
.msg.user .cursor { color: rgba(255,255,255,0.8); }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

/* ── Thinking dots ── */
.think-dots { display: inline-flex; gap: 4px; padding: 4px 0; }
.think-dots i {
  font-style: normal; font-size: 6px; color: var(--text-tertiary);
  animation: dotBounce 1.2s ease-in-out infinite;
}
.think-dots i:nth-child(2) { animation-delay: 0.15s; }
.think-dots i:nth-child(3) { animation-delay: 0.3s; }
@keyframes dotBounce { 0%,60%,100%{opacity:0.25;transform:translateY(0)} 30%{opacity:1;transform:translateY(-4px)} }

/* ── Input bar ── */
.bar { padding: 12px 20px 16px; border-top: 0.5px solid var(--border); background: var(--bg-glass); }
.bar-inner {
  display: flex; align-items: center; gap: 8px;
  background: rgba(128,128,128,0.04); border: 0.5px solid var(--border);
  border-radius: 28px; padding: 7px 7px 7px 18px;
  transition: border-color var(--transition), box-shadow var(--transition);
}
.bar-inner:focus-within { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-light); }
.bar-input {
  flex: 1; border: none; outline: none; background: transparent;
  color: var(--text-primary); font-size: 14px; font-family: var(--font);
  padding: 4px 0;
}
.bar-input::placeholder { color: var(--text-tertiary); }
.bar-input:disabled { opacity: 0.4; }
.bar-btn {
  width: 34px; height: 34px; border-radius: 50%; border: none;
  background: rgba(128,128,128,0.12); color: var(--text-tertiary);
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all var(--transition); flex-shrink: 0;
}
.bar-btn.on { background: var(--accent); color: #fff; }
.bar-btn.on:hover { background: var(--accent-hover); }
.bar-btn:disabled { cursor: not-allowed; }
</style>
