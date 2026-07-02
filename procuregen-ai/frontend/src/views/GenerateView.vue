<template>
  <div class="generate">
    <div class="apple-card" style="padding: 32px;">
      <div class="steps-indicator">
        <div v-for="(s, i) in steps" :key="i" class="step-dot-wrap" :class="{ active: i <= store.currentStep, current: i === store.currentStep }">
          <div class="step-dot">{{ i + 1 }}</div>
          <div class="step-label">{{ s }}</div>
          <div v-if="i < 3" class="step-connector" :class="{ filled: i < store.currentStep }"></div>
        </div>
      </div>
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
const steps = ['输入需求', '解析结果', '风险报告', '生成下载']
</script>

<style scoped>
.generate { max-width: 900px; margin: 0 auto; }
.steps-indicator { display: flex; align-items: flex-start; justify-content: center; gap: 0; margin-bottom: 40px; padding-bottom: 24px; border-bottom: 0.5px solid var(--border); }
.step-dot-wrap { display: flex; flex-direction: column; align-items: center; position: relative; flex: 1; max-width: 100px; }
.step-dot { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; background: rgba(0,0,0,0.04); color: var(--text-tertiary); transition: all var(--transition); }
.step-dot-wrap.active .step-dot { background: var(--accent); color: #fff; }
.step-dot-wrap.current .step-dot { box-shadow: 0 0 0 6px var(--accent-light); }
.step-label { font-size: 12px; font-weight: 500; color: var(--text-tertiary); margin-top: 8px; text-align: center; transition: color var(--transition); }
.step-dot-wrap.active .step-label { color: var(--text-primary); }
.step-connector { position: absolute; top: 18px; left: calc(50% + 18px); width: calc(100% - 36px); height: 1px; background: var(--border); transition: background var(--transition); }
.step-connector.filled { background: var(--accent); }
</style>
