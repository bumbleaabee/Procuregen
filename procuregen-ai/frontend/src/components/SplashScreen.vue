<template>
  <div class="splash">
    <div class="splash-bg"><div class="mesh"></div><div class="dots"></div></div>
    <div class="splash-main">
      <div class="logo"><svg width="56" height="56" viewBox="0 0 56 56" fill="none"><rect x="8" y="10" width="40" height="36" rx="7" stroke="currentColor" stroke-width="2.2"/><line x1="19" y1="23" x2="37" y2="23" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="19" y1="30" x2="31" y2="30" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></div>
      <h1 :class="{ in: s >= 1 }">ProcureGen</h1>
      <p :class="{ in: s >= 2 }">采购文件智能生成系统<span>AI-Powered Procurement</span></p>
      <div class="pills" :class="{ in: s >= 2 }"><span>语义理解</span><span>模板组装</span><span>风险预审</span><span>一键导出</span></div>
      <button :class="{ in: s >= 3 }" @click="go">开始使用 →</button>
    </div>
    <div class="splash-foot">Powered by DeepSeek</div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
const s=ref(0);const emit=defineEmits(['done'])
onMounted(()=>{if(localStorage.getItem('pw_v4')){emit('done');return};setTimeout(()=>s.value=1,400);setTimeout(()=>s.value=2,800);setTimeout(()=>s.value=3,1400)})
function go(){localStorage.setItem('pw_v4','1');emit('done')}
</script>
<style scoped>
.splash{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;flex-direction:column;background:#0a0a0a}
.splash-bg{position:absolute;inset:0;overflow:hidden}
.mesh{position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 30% 20%,rgba(0,113,227,.12),transparent),radial-gradient(ellipse 60% 70% at 70% 70%,rgba(175,82,222,.08),transparent)}
.dots{position:absolute;inset:0;background-image:radial-gradient(circle,rgba(255,255,255,.03) 1px,transparent 1px);background-size:32px 32px}
.splash-main{position:relative;z-index:1;text-align:center}
.logo{color:#0071e3;margin-bottom:24px;animation:popIn .8s cubic-bezier(.16,1,.3,1)}
@keyframes popIn{from{opacity:0;transform:scale(.8) translateY(16px)}to{opacity:1;transform:scale(1) translateY(0)}}
h1{font-size:48px;font-weight:800;letter-spacing:-2px;color:#fff;opacity:0;transform:translateY(16px);transition:all .7s cubic-bezier(.16,1,.3,1)}
h1.in{opacity:1;transform:translateY(0)}
p{font-size:16px;color:rgba(255,255,255,.5);margin-top:8px;opacity:0;transform:translateY(12px);transition:all .7s .1s cubic-bezier(.16,1,.3,1)}
p.in{opacity:1;transform:translateY(0)}
p span{display:block;font-size:11px;color:rgba(255,255,255,.25);margin-top:4px;letter-spacing:2px;text-transform:uppercase}
.pills{display:flex;gap:8px;justify-content:center;margin-top:24px;flex-wrap:wrap;opacity:0;transform:translateY(12px);transition:all .7s .2s cubic-bezier(.16,1,.3,1)}
.pills.in{opacity:1;transform:translateY(0)}
.pills span{padding:6px 14px;border-radius:100px;background:rgba(255,255,255,.06);border:.5px solid rgba(255,255,255,.08);color:rgba(255,255,255,.6);font-size:13px;font-weight:500}
button{margin-top:36px;padding:14px 32px;border-radius:100px;border:none;background:#0071e3;color:#fff;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;opacity:0;transform:translateY(12px);transition:all .7s .3s cubic-bezier(.16,1,.3,1)}
button.in{opacity:1;transform:translateY(0)}
button:hover{background:#0077ed;box-shadow:0 4px 24px rgba(0,113,227,.35)}
.splash-foot{position:absolute;bottom:28px;z-index:1;font-size:12px;color:rgba(255,255,255,.15);letter-spacing:1px}
</style>
