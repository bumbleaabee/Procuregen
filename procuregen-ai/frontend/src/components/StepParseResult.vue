<template>
  <div class="step">
    <div class="step-head">
      <h2>确认解析结果</h2>
      <p>AI 已提取以下字段，请核对并补充缺失信息 · 置信度 {{ Math.round((store.parsedSpec?.confidence || 0) * 100) }}%</p>
    </div>
    <div v-if="store.parsedSpec?.missing_fields?.length" class="alert">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="8" x2="12" y2="12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><circle cx="12" cy="16" r="0.5" fill="currentColor" stroke="none"/></svg>
      以下字段缺失：<strong>{{ store.parsedSpec.missing_fields.join('、') }}</strong>
    </div>
    <div class="fields">
      <div class="field" v-for="f in fields" :key="f.key">
        <label>{{ f.label }}</label>
        <input v-if="f.type === 'text'" class="apple-input" v-model="store.parsedSpec[f.key]" :placeholder="f.placeholder" />
        <input v-else-if="f.type === 'number'" class="apple-input" type="number" v-model.number="store.parsedSpec[f.key]" :placeholder="f.placeholder" style="-moz-appearance:textfield" />
        <select v-else-if="f.type === 'select'" class="apple-input" v-model="store.parsedSpec[f.key]">
          <option v-for="o in f.options" :key="o" :value="o">{{ o }}</option>
        </select>
        <div v-else-if="f.type === 'tags'" class="tags-wrap">
          <span v-for="(tag, i) in (store.parsedSpec[f.key] || [])" :key="i" class="tag">{{ tag }}<button @click="store.parsedSpec[f.key].splice(i, 1)">&times;</button></span>
          <input class="tag-input" :placeholder="f.placeholder" @keyup.enter="addTag(f.key, $event)" />
        </div>
      </div>
    </div>
    <div class="step-actions">
      <button class="apple-btn apple-btn-secondary" @click="store.reset()">重新输入</button>
      <button class="apple-btn apple-btn-primary" @click="store.doRiskCheck()" style="padding:12px 24px;font-size:15px;">
        下一步：风险预审
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><polyline points="9 18 15 12 9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useGenerateStore } from '../stores/generate'
const store = useGenerateStore()
const fields = [
  { key: 'project_name', label: '项目名称', type: 'text', placeholder: '输入项目名称' },
  { key: 'purchase_type', label: '采购类型', type: 'select', options: ['货物', '服务', '工程'] },
  { key: 'procurement_method', label: '采购方式', type: 'select', options: ['公开招标', '竞争性谈判', '询价', '竞争性磋商'] },
  { key: 'budget', label: '预算金额（元）', type: 'number', placeholder: '例：800000' },
  { key: 'delivery_period', label: '交付周期', type: 'text', placeholder: '例：30天' },
  { key: 'warranty_period', label: '质保期限', type: 'text', placeholder: '例：3年' },
  { key: 'payment_terms', label: '付款方式', type: 'text', placeholder: '例：合同签订后支付30%' },
  { key: 'acceptance_criteria', label: '验收标准', type: 'text', placeholder: '例：到货验收合格' },
  { key: 'qualification', label: '供应商资格', type: 'tags', placeholder: '添加资格条件后回车' },
  { key: 'technical_specs', label: '技术参数', type: 'tags', placeholder: '添加技术参数后回车' },
  { key: 'evaluation_factors', label: '评分因素', type: 'tags', placeholder: '添加评分因素后回车' },
]
function addTag(key, e) {
  const v = e.target.value.trim()
  if (v) { if (!store.parsedSpec[key]) store.parsedSpec[key] = []; store.parsedSpec[key].push(v); e.target.value = '' }
}
</script>

<style scoped>
.step-head { text-align: center; margin-bottom: 24px; }
.step-head h2 { font-size: 24px; font-weight: 650; letter-spacing: -0.5px; }
.step-head p { font-size: 14px; color: var(--text-secondary); margin-top: 6px; }
.alert { display: flex; align-items: center; gap: 8px; padding: 12px 16px; background: #f5a62310; border: 0.5px solid #f5a62330; border-radius: var(--radius-sm); font-size: 13px; color: #b87a14; margin-bottom: 24px; }
.fields { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 12px; font-weight: 550; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.3px; }
.tags-wrap { display: flex; flex-wrap: wrap; gap: 4px; align-items: center; min-height: 42px; padding: 6px 8px; border: 0.5px solid var(--border); border-radius: var(--radius-sm); background: rgba(0,0,0,0.01); }
.tag { display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px; background: var(--accent-light); color: var(--accent); border-radius: 100px; font-size: 12px; font-weight: 500; }
.tag button { background: none; border: none; color: var(--accent); cursor: pointer; font-size: 14px; line-height: 1; padding: 0; margin-left: 2px; }
.tag-input { border: none; outline: none; font-size: 13px; font-family: var(--font); padding: 4px; min-width: 120px; background: transparent; }
.step-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 28px; }
</style>
