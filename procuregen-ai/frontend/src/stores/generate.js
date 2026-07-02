import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useGenerateStore = defineStore('generate', () => {
  // 当前步骤：0=输入, 1=解析结果, 2=风险报告, 3=预览下载
  const currentStep = ref(0)
  const inputText = ref('')
  const parsedSpec = ref(null)
  const riskReport = ref(null)
  const selectedClauses = ref([])
  const generateResult = ref(null)
  const loading = ref(false)

  // 步骤 1：解析需求
  async function doParse() {
    if (!inputText.value.trim()) return
    loading.value = true
    try {
      const res = await api.post('/parse', { input_text: inputText.value, mode: 'llm' })
      if (res.success) {
        parsedSpec.value = res.data
        // 同时保存原始输入
        parsedSpec.value._input_text = inputText.value
        currentStep.value = 1
      }
    } finally {
      loading.value = false
    }
  }

  // 步骤 2：风险预审
  async function doRiskCheck() {
    if (!parsedSpec.value) return
    loading.value = true
    try {
      const res = await api.post('/risk-check', {
        parsed_spec: parsedSpec.value,
        selected_clauses: selectedClauses.value
      })
      if (res.success) {
        riskReport.value = res.data
        parsedSpec.value._risk_report = res.data
        currentStep.value = 2
      }
    } finally {
      loading.value = false
    }
  }

  // 步骤 3：生成文档
  async function doGenerate() {
    if (!parsedSpec.value) return
    loading.value = true
    try {
      const res = await api.post('/generate', {
        parsed_spec: parsedSpec.value,
        template_id: 1,
        selected_clauses: selectedClauses.value
      })
      if (res.success) {
        generateResult.value = res.data
        selectedClauses.value = res.data.clauses || []
        currentStep.value = 3
      }
    } finally {
      loading.value = false
    }
  }

  // 下载文件
  function getDownloadUrl(taskId) {
    return `/api/export/${taskId}`
  }

  // 重置
  function reset() {
    currentStep.value = 0
    inputText.value = ''
    parsedSpec.value = null
    riskReport.value = null
    selectedClauses.value = []
    generateResult.value = null
    loading.value = false
  }

  // 修改解析字段
  function updateField(field, value) {
    if (parsedSpec.value) {
      parsedSpec.value[field] = value
    }
  }

  return {
    currentStep, inputText, parsedSpec, riskReport,
    selectedClauses, generateResult, loading,
    doParse, doRiskCheck, doGenerate, getDownloadUrl,
    reset, updateField
  }
})
