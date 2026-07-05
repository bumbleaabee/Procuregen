<template>
  <div class="polish-root">
    <div class="top">
      <h2>文档润色工作台</h2>
      <div class="actions">
        <button v-for="a in actions" :key="a.key" class="act" :class="{ on: mode === a.key }" @click="setMode(a.key)" :disabled="busy">{{ a.icon }} {{ a.label }}</button>
      </div>
    </div>

    <div class="panes">
      <div class="pane">
        <div class="pane-head">原始文本</div>
        <textarea v-model="input" class="pane-textarea" placeholder="在此粘贴或输入采购文档文本..."></textarea>
      </div>
      <div class="pane">
        <div class="pane-head">
          处理结果
          <span class="pane-actions">
            <button v-if="result && !busy" @click="applyResult" class="pane-btn">应用至左侧</button>
            <button v-if="result && !busy" @click="copyResult" class="pane-btn">复制</button>
          </span>
        </div>
        <div class="pane-body" :class="{ empty: !result && !busy }">
          <div v-if="busy" class="stream">{{ streamText }}<span class="cursor">|</span></div>
          <div v-else-if="result" class="stream">{{ result }}</div>
          <div v-else class="hint">选择上方操作模式，AI 将在此流式输出处理结果</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const input=ref(''),result=ref(''),streamText=ref(''),mode=ref('polish'),busy=ref(false)
let ctrl=null
const actions=[
  {key:'polish',label:'润色优化',icon:'Sparkles'},
  {key:'expand',label:'扩写补充',icon:'FileText'},
  {key:'shorten',label:'精简缩写',icon:'Scissors'},
  {key:'formal',label:'正式化',icon:'Building'},
  {key:'autocomplete',label:'智能续写',icon:'Bot'},
]

async function setMode(key){mode.value=key;await run()}
async function run(){
  const t=input.value.trim();if(!t||busy.value)return;busy.value=true;result.value='';streamText.value=''
  if(ctrl)ctrl.abort();ctrl=new AbortController()
  try{
    const u=`/api/polish-stream?text=${encodeURIComponent(t)}&action=${mode.value}`
    const r=await fetch(u,{signal:ctrl.signal});const reader=r.body.getReader();const dec=new TextDecoder();let buf=''
    while(true){const{ done,value }=await reader.read();if(done)break;buf+=dec.decode(value,{stream:true});const lines=buf.split('\n');buf=lines.pop()||''
      for(const line of lines){if(!line.startsWith('data: '))continue;try{const d=JSON.parse(line.slice(6));if(d.done){result.value=d.full;streamText.value='';busy.value=false;return}if(d.token)streamText.value+=d.token}catch{}}
    }
  }catch{if(!result.value)result.value=streamText.value}
  busy.value=false
}
async function copyResult(){try{await navigator.clipboard.writeText(result.value)}catch{}}
function applyResult(){input.value=result.value;result.value='';streamText.value=''}
</script>

<style scoped>
.polish-root{max-width:960px;margin:0 auto}
.top{text-align:center;margin-bottom:22px}
.top h2{font-size:22px;font-weight:700;letter-spacing:-.5px;margin-bottom:14px}
.actions{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.act{display:flex;align-items:center;gap:6px;padding:9px 20px;border-radius:100px;border:0.5px solid var(--border);background:var(--bg-glass);color:var(--text-secondary);font-size:13px;cursor:pointer;transition:all .25s var(--ease);font-family:var(--font);font-weight:500}
.act:hover:not(:disabled){border-color:var(--accent);color:var(--accent)}
.act.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.act:disabled{opacity:.4;cursor:not-allowed}

.panes{display:grid;grid-template-columns:1fr 1fr;gap:16px;height:calc(100vh - 200px)}
.pane{display:flex;flex-direction:column;
  background:var(--bg-elevated);backdrop-filter:blur(28px) saturate(200%);
  -webkit-backdrop-filter:blur(28px) saturate(200%);
  border-radius:var(--radius-lg);border:0.5px solid var(--border-glass);overflow:hidden;
  box-shadow:0 1px 0 rgba(255,255,255,.04) inset,0 2px 8px rgba(0,0,0,.04),0 8px 32px rgba(0,0,0,.05)}
.dark .pane{box-shadow:0 1px 0 rgba(255,255,255,.02) inset,0 2px 8px rgba(0,0,0,.3),0 8px 32px rgba(0,0,0,.4)}
.pane-head{display:flex;align-items:center;gap:8px;padding:14px 18px;font-size:12px;font-weight:600;color:var(--text-secondary);text-transform:uppercase;letter-spacing:.5px;border-bottom:0.5px solid var(--border)}
.pane-actions{margin-left:auto;display:flex;gap:6px}
.pane-btn{font-size:11px;font-weight:500;background:none;border:0.5px solid var(--border);border-radius:6px;padding:4px 10px;cursor:pointer;color:var(--text-secondary);font-family:var(--font);transition:all var(--ease)}.pane-btn:hover{border-color:var(--accent);color:var(--accent)}

.pane-textarea{flex:1;padding:18px;border:none;outline:none;resize:none;font-size:15px;line-height:1.75;font-family:var(--font);background:transparent;color:var(--text)}.pane-textarea::placeholder{color:var(--text-tertiary)}
.pane-body{flex:1;overflow-y:auto;padding:18px}.pane-body.empty{display:flex;align-items:center;justify-content:center}
.hint{text-align:center;color:var(--text-tertiary);font-size:14px;line-height:1.6}
.stream{white-space:pre-wrap;font-size:15px;line-height:1.75;color:var(--text)}
.cursor{color:var(--accent);font-weight:100;animation:blink 1s step-end infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
</style>
