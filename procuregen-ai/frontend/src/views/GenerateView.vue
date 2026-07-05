<template>
  <div class="generate">
    <div class="steps-row">
      <div v-for="(s, i) in steps" :key="i" class="step-dot-wrap" :class="{ done: i < store.currentStep, now: i === store.currentStep }">
        <div class="step-dot">{{ i < store.currentStep ? 'OK' : i + 1 }}</div>
        <div class="step-label">{{ s }}</div>
        <div v-if="i < 3" class="step-line" :class="{ on: i < store.currentStep }"></div>
      </div>
    </div>

    <div class="step-body glass-card">
      <StepInput v-if="store.currentStep === 0" />
      <StepParseResult v-else-if="store.currentStep === 1" />
      <StepRiskReport v-else-if="store.currentStep === 2" />
      <StepPreview v-else-if="store.currentStep === 3" />
    </div>
  </div>
</template>

<script setup>
import { useGenerateStore } from '../stores/generate'
import StepInput from '../components/StepInput.vue'
import StepParseResult from '../components/StepParseResult.vue'
import StepRiskReport from '../components/StepRiskReport.vue'
import StepPreview from '../components/StepPreview.vue'
const store = useGenerateStore()
const steps = ['输入需求','解析结果','风险报告','生成下载']
</script>

<style scoped>
.generate{max-width:800px;margin:0 auto;padding-top:8px}
.steps-row{display:flex;align-items:center;justify-content:center;margin-bottom:32px}
.step-dot-wrap{display:flex;flex-direction:column;align-items:center;position:relative;flex:1;max-width:96px}
.step-dot{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;background:var(--bg3);color:var(--text-tertiary);transition:all .4s var(--ease)}
.step-dot-wrap.done .step-dot{background:var(--accent);color:#fff}
.step-dot-wrap.now .step-dot{box-shadow:0 0 0 8px var(--accent-ghost);background:var(--accent);color:#fff;animation:pulseRing 2s ease-in-out infinite}
@keyframes pulseRing{0%,100%{box-shadow:0 0 0 6px var(--accent-ghost)}50%{box-shadow:0 0 0 14px rgba(43,138,255,.04)}}
.step-label{font-size:13px;font-weight:550;color:var(--text-tertiary);margin-top:10px;text-align:center;transition:color .4s var(--ease)}
.step-dot-wrap.done .step-label,.step-dot-wrap.now .step-label{color:var(--text)}
.step-line{position:absolute;top:18px;left:calc(50% + 18px);width:calc(100% - 36px);height:2px;background:var(--border);border-radius:1px;transition:background .4s var(--ease)}
.step-line.on{background:var(--accent)}
.step-body{padding:48px 44px}
</style>
