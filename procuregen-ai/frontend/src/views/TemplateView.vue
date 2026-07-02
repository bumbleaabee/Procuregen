<template>
  <div class="template-page">
    <el-tabs v-model="activeTab" type="border-card">
      <!-- 模板管理 Tab -->
      <el-tab-pane label="招标书模板" name="templates">
        <div class="tab-header">
          <span>模板列表（{{ templates.length }}）</span>
          <el-button type="primary" size="small" @click="openTplDialog()">
            <el-icon><Plus /></el-icon> 新增模板
          </el-button>
        </div>

        <el-table :data="templates" v-loading="tplLoading" stripe empty-text="暂无模板">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="name" label="模板名称" min-width="180" />
          <el-table-column label="类型" width="120">
            <template #default="{ row }">
              <el-tag size="small">{{ row.template_type === 'tender' ? '招标书' : row.template_type === 'contract' ? '合同' : '风险报告' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="创建时间" width="170">
            <template #default="{ row }">{{ row.created_at?.slice(0, 19) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="160">
            <template #default="{ row }">
              <el-button size="small" link type="primary" @click="openTplDialog(row)">编辑</el-button>
              <el-popconfirm title="确定删除？" @confirm="deleteTemplate(row.id)">
                <template #reference>
                  <el-button size="small" link type="danger">删除</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- 条款管理 Tab -->
      <el-tab-pane label="合同条款库" name="clauses">
        <div class="tab-header">
          <span>条款列表（{{ clauses.length }}）</span>
          <el-button type="primary" size="small" @click="openClauseDialog()">
            <el-icon><Plus /></el-icon> 新增条款
          </el-button>
        </div>

        <el-input
          v-model="clauseFilter"
          placeholder="按类别筛选（通用/财务/法律）"
          clearable
          :prefix-icon="Search"
          style="width: 260px; margin-bottom: 12px;"
        />

        <el-table :data="filteredClauses" v-loading="clauseLoading" stripe empty-text="暂无条款">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="title" label="条款标题" min-width="180" />
          <el-table-column label="类别" width="100">
            <template #default="{ row }">
              <el-tag size="small" :type="row.category === '财务' ? 'warning' : row.category === '法律' ? 'danger' : ''">
                {{ row.category }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="适用条件" width="130">
            <template #default="{ row }">
              <el-tag size="small" type="info" effect="plain">{{ row.applicable_condition || '通用' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="内容预览" min-width="220">
            <template #default="{ row }">{{ row.content?.slice(0, 60) }}{{ row.content?.length > 60 ? '...' : '' }}</template>
          </el-table-column>
          <el-table-column label="操作" width="160">
            <template #default="{ row }">
              <el-button size="small" link type="primary" @click="openClauseDialog(row)">编辑</el-button>
              <el-popconfirm title="确定删除？" @confirm="deleteClause(row.id)">
                <template #reference>
                  <el-button size="small" link type="danger">删除</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <!-- 模板编辑对话框 -->
    <el-dialog
      v-model="tplDialogVisible"
      :title="editingTpl?.id ? '编辑模板' : '新增模板'"
      width="700px"
      destroy-on-close
    >
      <el-form :model="tplForm" label-width="100px">
        <el-form-item label="模板名称">
          <el-input v-model="tplForm.name" placeholder="如：标准招标书模板" />
        </el-form-item>
        <el-form-item label="模板类型">
          <el-select v-model="tplForm.template_type" style="width:100%">
            <el-option label="招标书 (tender)" value="tender" />
            <el-option label="合同 (contract)" value="contract" />
            <el-option label="风险报告 (risk_report)" value="risk_report" />
          </el-select>
        </el-form-item>
        <el-form-item label="模板内容 (Jinja2)">
          <el-input v-model="tplForm.content" type="textarea" :rows="14" placeholder="支持 Jinja2 模板语法：{{ variable }}、{% if %}、{% for %}" />
        </el-form-item>
        <el-form-item label="变量说明">
          <el-input v-model="tplForm.variables" placeholder="用逗号分隔，如：project_name,budget,delivery_period" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="tplDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveTemplate">保存</el-button>
      </template>
    </el-dialog>

    <!-- 条款编辑对话框 -->
    <el-dialog
      v-model="clauseDialogVisible"
      :title="editingClause?.id ? '编辑条款' : '新增条款'"
      width="680px"
      destroy-on-close
    >
      <el-form :model="clauseForm" label-width="100px">
        <el-form-item label="条款标题">
          <el-input v-model="clauseForm.title" placeholder="如：交付与验收条款" />
        </el-form-item>
        <el-form-item label="类别">
          <el-select v-model="clauseForm.category" style="width:100%" allow-create filterable>
            <el-option label="通用" value="通用" />
            <el-option label="财务" value="财务" />
            <el-option label="法律" value="法律" />
            <el-option label="技术" value="技术" />
          </el-select>
        </el-form-item>
        <el-form-item label="适用条件">
          <el-select v-model="clauseForm.applicable_condition" style="width:100%" allow-create filterable>
            <el-option label="货物" value="货物" />
            <el-option label="服务" value="服务" />
            <el-option label="工程" value="工程" />
            <el-option label="预算较高" value="预算较高" />
            <el-option label="软件" value="软件" />
            <el-option label="通用" value="通用" />
          </el-select>
        </el-form-item>
        <el-form-item label="条款正文">
          <el-input v-model="clauseForm.content" type="textarea" :rows="10" placeholder="输入条款具体内容..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="clauseDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveClause">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import api from '../api'

const activeTab = ref('templates')

// ── 模板管理 ──
const templates = ref([])
const tplLoading = ref(false)
const tplDialogVisible = ref(false)
const editingTpl = ref(null)
const tplForm = ref({ name: '', template_type: 'tender', content: '', variables: '' })

async function fetchTemplates() {
  tplLoading.value = true
  try {
    const res = await api.get('/templates')
    if (res.success) templates.value = res.data || []
  } finally { tplLoading.value = false }
}

function openTplDialog(row = null) {
  if (row) {
    editingTpl.value = row
    tplForm.value = { name: row.name, template_type: row.template_type, content: row.content, variables: row.variables || '' }
  } else {
    editingTpl.value = null
    tplForm.value = { name: '', template_type: 'tender', content: '', variables: '' }
  }
  tplDialogVisible.value = true
}

async function saveTemplate() {
  try {
    const payload = { ...tplForm.value }
    let res
    if (editingTpl.value?.id) {
      res = await api.put(`/templates/${editingTpl.value.id}`, payload)
    } else {
      res = await api.post('/templates', payload)
    }
    if (res.success) {
      ElMessage.success(editingTpl.value?.id ? '更新成功' : '创建成功')
      tplDialogVisible.value = false
      fetchTemplates()
    }
  } catch (e) { /* ignore */ }
}

async function deleteTemplate(id) {
  const res = await api.delete(`/templates/${id}`)
  if (res.success) { ElMessage.success('已删除'); fetchTemplates() }
}

// ── 条款管理 ──
const clauses = ref([])
const clauseLoading = ref(false)
const clauseDialogVisible = ref(false)
const editingClause = ref(null)
const clauseFilter = ref('')
const clauseForm = ref({ title: '', category: '通用', content: '', applicable_condition: '通用' })

const filteredClauses = computed(() => {
  if (!clauseFilter.value) return clauses.value
  const kw = clauseFilter.value.toLowerCase()
  return clauses.value.filter(c => c.category?.toLowerCase().includes(kw))
})

async function fetchClauses() {
  clauseLoading.value = true
  try {
    const res = await api.get('/clauses')
    if (res.success) clauses.value = res.data || []
  } finally { clauseLoading.value = false }
}

function openClauseDialog(row = null) {
  if (row) {
    editingClause.value = row
    clauseForm.value = {
      title: row.title, category: row.category, content: row.content,
      applicable_condition: row.applicable_condition || '通用'
    }
  } else {
    editingClause.value = null
    clauseForm.value = { title: '', category: '通用', content: '', applicable_condition: '通用' }
  }
  clauseDialogVisible.value = true
}

async function saveClause() {
  try {
    const payload = { ...clauseForm.value }
    let res
    if (editingClause.value?.id) {
      res = await api.put(`/clauses/${editingClause.value.id}`, payload)
    } else {
      res = await api.post('/clauses', payload)
    }
    if (res.success) {
      ElMessage.success(editingClause.value?.id ? '更新成功' : '创建成功')
      clauseDialogVisible.value = false
      fetchClauses()
    }
  } catch (e) { /* ignore */ }
}

async function deleteClause(id) {
  const res = await api.delete(`/clauses/${id}`)
  if (res.success) { ElMessage.success('已删除'); fetchClauses() }
}

onMounted(() => { fetchTemplates(); fetchClauses() })
</script>

<style scoped>
.template-page { max-width: 1200px; margin: 0 auto; }
.tab-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; font-weight: 500; }
</style>
