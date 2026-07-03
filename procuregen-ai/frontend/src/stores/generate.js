import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useGenerateStore = defineStore('generate', () => {
  const currentStep = ref(0)
  const inputText = ref('')
  const parsedSpec = ref(null)
  const riskReport = ref(null)
  const selectedClauses = ref([])
  const generateResult = ref(null)
  const loading = ref(false)
  const loadingStatus = ref('processing')

  // 流式输出相关
  const streamingText = ref('')
  const isStreaming = ref(false)

  // 步骤 1：传统解析
  async function doParse() {
    if (!inputText.value.trim() || loading.value) return
    loading.value = true; loadingStatus.value = 'parsing'
    try {
      const res = await api.post('/parse', { input_text: inputText.value, mode: 'llm' })
      if (res.success) {
        parsedSpec.value = res.data
        parsedSpec.value._input_text = inputText.value
        currentStep.value = 1
      }
    } finally {
      loading.value = false
    }
  }

  // 步骤 1b：流式解析（SSE 逐 token 推送）
  async function doParseStream() {
    if (!inputText.value.trim() || loading.value) return
    isStreaming.value = true; streamingText.value = ''; loading.value = true; loadingStatus.value = 'parsing'

    try {
      const url = `/api/parse-stream?input_text=${encodeURIComponent(inputText.value)}`
      const eventSource = new EventSource(url)

      return new Promise((resolve, reject) => {
        eventSource.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            if (data.done) {
              eventSource.close()
              isStreaming.value = false
              loading.value = false
              // 尝试解析完整 JSON
              const json = extractJson(data.full)
              if (json) {
                parsedSpec.value = json
                parsedSpec.value._input_text = inputText.value
                currentStep.value = 1
              }
              resolve()
            } else if (data.token) {
              streamingText.value += data.token
            }
          } catch (e) { /* ignore parse errors */ }
        }
        eventSource.onerror = () => {
          eventSource.close()
          isStreaming.value = false
          loading.value = false
          // 降级到传统解析
          doParse()
          resolve()
        }
        setTimeout(() => {
          if (isStreaming.value) {
            eventSource.close()
            isStreaming.value = false
            loading.value = false
            doParse()
            resolve()
          }
        }, 30000)
      })
    } catch {
      isStreaming.value = false
      loading.value = false
      doParse()
    }
  }

  function extractJson(text) {
    try { return JSON.parse(text) } catch {}
    const m = text.match(/\{[\s\S]*\}/)
    if (m) { try { return JSON.parse(m[0]) } catch {} }
    return null
  }

  // 步骤 2：风险预审
  async function doRiskCheck() {
    if (!parsedSpec.value || loading.value) return
    loading.value = true; loadingStatus.value = 'risk'
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
    if (!parsedSpec.value || loading.value) return
    loading.value = true; loadingStatus.value = 'generating'
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
    streamingText.value = ''
    isStreaming.value = false
    loadingStatus.value = 'processing'
  }

  // 修改解析字段
  function updateField(field, value) {
    if (parsedSpec.value) {
      parsedSpec.value[field] = value
    }
  }

  return {
    currentStep, inputText, parsedSpec, riskReport,
    selectedClauses, generateResult, loading, loadingStatus,
    streamingText, isStreaming,
    doParse, doParseStream, doRiskCheck, doGenerate, getDownloadUrl,
    reset, updateField
  }
})
