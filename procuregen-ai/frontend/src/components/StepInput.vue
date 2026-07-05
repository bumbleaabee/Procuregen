<template>
  <div class="step">
    <div class="step-head">
      <h2>描述您的采购需求</h2>
      <p>用自然语言输入，AI 会实时解析关键信息</p>
    </div>
    <textarea class="apple-textarea" v-model="store.inputText" placeholder="例如：学校拟采购一批人工智能实验室服务器，预算80万元，要求4台GPU服务器..." maxlength="5000"></textarea>
    <div class="char-count">{{ store.inputText.length }} / 5000</div>

    <!-- 流式输出预览 -->
    <div v-if="store.isStreaming || store.streamingText" class="stream-preview">
      <div class="stream-header">
        <span class="stream-dot"></span>
        <span>AI 正在解析...</span>
      </div>
      <div class="stream-content">{{ store.streamingText || '正在连接 AI 引擎...' }}<span class="cursor" v-if="store.isStreaming">|</span></div>
    </div>

    <div class="step-actions">
      <router-link to="/" class="apple-btn apple-btn-secondary">返回</router-link>
      <button class="apple-btn apple-btn-primary" :disabled="!store.inputText.trim() || store.isStreaming" @click="store.doParseStream()" style="padding:12px 28px;font-size:15px;">
        <svg v-if="!store.isStreaming" width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <span v-if="store.isStreaming" class="spinner"></span>
        {{ store.isStreaming ? 'AI 思考中...' : '智能解析' }}
      </button>
    </div>

    <div class="samples">
      <p class="samples-title">快速体验</p>
      <div class="sample-list">
        <button v-for="s in sampleList" :key="s.type" class="sample-chip" @click="fillSample(s.type)">{{ s.emoji }} {{ s.label }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useGenerateStore } from '../stores/generate'
const store = useGenerateStore()
const samples = {
  server: '学校拟采购一批人工智能实验室服务器，用于深度学习课程和学生科研训练。预算80万元，要求4台GPU服务器，每台不少于2张48GB显存GPU，交付周期30天，供应商需要具备近三年高校信息化项目案例，提供三年质保和本地售后服务。请生成公开招标文件初稿，并给出合同关键条款。',
  software: '学校拟建设一套智慧校园综合管理平台，包含教务管理、学生管理、后勤管理、数据分析等模块。预算150万元，要求供应商具备CMMI3级以上资质，具有高校信息化项目经验，提供三年免费运维和7×24小时技术支持。采用竞争性磋商方式采购，交付周期90天。',
  service: '学校拟采购2026-2027年度校园物业管理服务，涵盖教学楼、办公楼、学生宿舍、图书馆等区域，总面积约15万平方米。预算200万元/年，要求供应商具有物业服务一级资质，近三年有高校或大型企事业单位物业服务经验。',
}
const sampleList = [
  { type: 'server', label: '服务器采购', emoji: '🖥️' },
  { type: 'software', label: '软件平台', emoji: '💻' },
  { type: 'service', label: '物业服务', emoji: '🏢' },
]
function fillSample(type) { store.inputText = samples[type] || samples.server }
</script>

<style scoped>
.step-head h2 { font-size: 24px; font-weight: 650; letter-spacing: -0.5px; color: var(--text); }
.step-head p { font-size: 15px; color: var(--text-secondary); margin-top: 6px; }
.step-head { text-align: center; margin-bottom: 28px; }
.char-count { text-align: right; font-size: 12px; color: var(--text-tertiary); margin-top: 6px; }
.step-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 24px; }

/* Streaming preview */
.stream-preview { margin-top: 20px; padding: 16px; border-radius: var(--radius); border: 0.5px solid var(--border); background: var(--accent-ghost); }
.stream-header { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--accent); margin-bottom: 8px; }
.stream-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); animation: pulse 1.2s ease-in-out infinite; }
.stream-content { font-size: 14px; color: var(--text-secondary); line-height: 1.7; white-space: pre-wrap; font-family: 'SF Mono', 'Cascadia Code', 'Consolas', monospace; max-height: 300px; overflow-y: auto; }
.cursor { display: inline-block; color: var(--accent); animation: blink 0.8s step-end infinite; }

/* Spinner */
.spinner { display: inline-block; width: 18px; height: 18px; border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.6s linear infinite; }

.samples { margin-top: 32px; padding-top: 24px; border-top: 0.5px solid var(--border); }
.samples-title { font-size: 13px; font-weight: 550; color: var(--text-secondary); margin-bottom: 10px; }
.sample-list { display: flex; gap: 8px; }
.sample-chip { padding: 8px 16px; border-radius: 100px; border: 0.5px solid var(--border); background: var(--accent-ghost); font-size: 13px; color: var(--text-secondary); cursor: pointer; transition: all var(--ease); font-family: var(--font); }
.sample-chip:hover { border-color: var(--accent); color: var(--accent); transform: translateY(-1px); }

@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
@keyframes blink { 50% { opacity: 0; } }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
