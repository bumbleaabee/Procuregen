<template>
  <div class="history-page">
    <div class="apple-card" style="padding:24px;">
      <div class="page-header">
        <h2 class="page-title">历史记录</h2>
        <div class="header-actions">
          <el-input v-model="keyword" placeholder="搜索项目名称..." clearable style="width: 240px;" @clear="fetchTasks()" @keyup.enter="fetchTasks()" />
          <router-link to="/generate" class="apple-btn apple-btn-primary" style="font-size:13px;padding:8px 16px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="8" x2="12" y2="16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="12" x2="16" y2="12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            新建
          </router-link>
        </div>
      </div>

      <el-table :data="tasks" v-loading="loading" stripe empty-text="暂无生成记录，去新建一个吧">
        <el-table-column prop="id" label="编号" width="75" align="center" />
        <el-table-column label="项目名称" min-width="200">
          <template #default="{ row }">
            <span class="project-name">{{ row.project_name || '未命名项目' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="风险等级" width="110" align="center">
          <template #default="{ row }">
            <el-tag
              :type="riskType(row.overall_level)"
              effect="dark"
              size="small"
              round
            >{{ levelLabel(row.overall_level) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-icon v-if="row.status === 'completed'" color="#67C23A" :size="18"><CircleCheckFilled /></el-icon>
            <el-icon v-else color="#909399" :size="18"><Clock /></el-icon>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="170">
          <template #default="{ row }">{{ row.created_at?.slice(0, 19) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button v-if="row.file_path" type="primary" size="small" link @click="downloadFile(row.id)">
              <el-icon><Download /></el-icon> 下载
            </el-button>
            <el-button size="small" link @click="showDetail(row)">
              <el-icon><View /></el-icon> 详情
            </el-button>
            <el-popconfirm title="确定删除此记录？" @confirm="deleteTask(row.id)">
              <template #reference>
                <el-button size="small" link type="danger">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap" v-if="total > pageSize">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchTasks"
        />
      </div>
    </div>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="任务详情" width="680px" destroy-on-close>
      <el-descriptions v-if="detailTask" :column="2" border size="small">
        <el-descriptions-item label="编号">{{ detailTask.id }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="detailTask.status === 'completed' ? 'success' : 'info'" size="small">{{ detailTask.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间" :span="2">{{ detailTask.created_at }}</el-descriptions-item>
        <el-descriptions-item label="原始需求" :span="2">
          <div class="detail-text">{{ detailTask.input_text }}</div>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'
import { Search } from '@element-plus/icons-vue'

const tasks = ref([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = 15
const keyword = ref('')
const detailVisible = ref(false)
const detailTask = ref(null)

onMounted(() => fetchTasks())

async function fetchTasks() {
  loading.value = true
  try {
    const params = { page: currentPage.value, size: pageSize }
    if (keyword.value.trim()) params.keyword = keyword.value.trim()
    const res = await api.get('/tasks', { params })
    if (res.success) {
      tasks.value = res.data.items || []
      total.value = res.data.total || 0
    }
  } finally {
    loading.value = false
  }
}

async function deleteTask(taskId) {
  try {
    const res = await api.delete(`/tasks/${taskId}`)
    if (res.success) {
      ElMessage.success('删除成功')
      fetchTasks()
    }
  } catch (e) { /* ignore */ }
}

function downloadFile(taskId) {
  window.open(`/api/export/${taskId}`, '_blank')
}

function showDetail(row) {
  detailTask.value = row
  detailVisible.value = true
}

function riskType(level) {
  if (level === 'high') return 'danger'
  if (level === 'medium') return 'warning'
  return 'success'
}

function levelLabel(level) {
  if (level === 'high') return '高风险'
  if (level === 'medium') return '中风险'
  return '低风险'
}
</script>

<style scoped>
.history-page { max-width: 1100px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-title { font-size: 24px; font-weight: 650; letter-spacing: -0.5px; }
.header-actions { display: flex; gap: 10px; align-items: center; }
.project-name { font-weight: 520; color: var(--text-primary); }
.pagination-wrap { display: flex; justify-content: center; margin-top: 20px; }
.detail-text { max-height: 200px; overflow-y: auto; white-space: pre-wrap; color: var(--text-secondary); font-size: 13px; line-height: 1.6; }
</style>
