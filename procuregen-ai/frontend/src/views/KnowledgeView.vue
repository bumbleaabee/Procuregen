<template>
  <div class="kb">
    <h2 class="page-title"><span class="grad">采购知识库</span></h2>
    <div class="kb-search">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="1.5"/><path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
      <input v-model="search" class="kb-input" placeholder="搜索采购法规、流程、术语..." @input="doSearch" />
      <kbd v-if="search">{{ filtered.length }} 条</kbd>
    </div>

    <div class="kb-cats">
      <button v-for="c in categories" :key="c" class="cat-chip" :class="{ active: activeCat === c }" @click="activeCat = c">{{ c }}</button>
    </div>

    <div class="kb-list">
      <div v-for="item in displayed" :key="item.id" class="apple-card kb-card" @click="toggleItem(item)">
        <div class="kb-card-header">
          <span class="kb-cat-tag">{{ item.category }}</span>
          <h4>{{ item.title }}</h4>
        </div>
        <Transition name="expand">
          <div v-if="item.open" class="kb-body">
            <div class="kb-content" v-html="renderContent(item)"></div>
            <div v-if="item.tags" class="kb-tags">
              <span v-for="t in item.tags" :key="t" class="kb-tag">#{{ t }}</span>
            </div>
          </div>
        </Transition>
      </div>
      <div v-if="displayed.length === 0" class="empty">未找到相关内容</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const search = ref('')
const activeCat = ref('全部')
const categories = ['全部', '招标流程', '合同条款', '法规解读', '评分标准', '风险防控', '术语解释']

const openMap = ref({})

const items = ref([
  { id: 1, title: '公开招标完整流程指南', category: '招标流程', tags: ['招标', '流程', '公开招标'],
    content: `<p><strong>公开招标</strong>是政府采购的主要方式，适用于采购金额较大、技术复杂度较高的项目。</p>
<p><strong>流程步骤：</strong></p><ol><li><strong>编制招标文件</strong>：包括采购公告、供应商须知、采购需求、评标办法、合同条款等</li><li><strong>发布招标公告</strong>：在指定媒体发布，公告期不少于 20 日</li><li><strong>供应商报名及资格预审</strong>：审核投标人资质</li><li><strong>发售招标文件</strong>：向合格供应商提供完整招标文件</li><li><strong>投标</strong>：供应商按要求提交投标文件</li><li><strong>开标</strong>：公开拆封投标文件</li><li><strong>评标</strong>：评标委员会按评分标准评审</li><li><strong>定标与公示</strong>：确定中标人并公示</li><li><strong>签订合同</strong>：与中标人签订采购合同</li></ol>` },
  { id: 2, title: '招标文件必备章节与内容', category: '招标流程', tags: ['招标文件', '结构', '模板'],
    content: `<p>一份完整的招标文件应包含以下章节：</p><ul><li><strong>采购公告</strong>：项目概况、预算金额、资格要求</li><li><strong>供应商须知</strong>：投标规则、文件组成要求</li><li><strong>采购需求</strong>：技术参数、交付要求、验收标准</li><li><strong>评标办法</strong>：评分因素、权重、计算方法</li><li><strong>合同主要条款</strong>：付款方式、违约责任、质保</li><li><strong>附件</strong>：投标文件格式、报价表、承诺函</li></ul>` },
  { id: 3, title: '合同违约责任条款设计要点', category: '合同条款', tags: ['合同', '违约', '责任'],
    content: `<p>违约责任条款是合同的核心保障条款，设计时应注意：</p><ul><li><strong>明确违约情形</strong>：列明交付延迟、质量不达标、不履行售后等</li><li><strong>违约金计算方式</strong>：按日计算（如每日千分之一）或按合同总额比例</li><li><strong>违约金上限</strong>：通常不超过合同总金额的 30%</li><li><strong>解除权约定</strong>：逾期超过 X 日，守约方有权单方解除</li><li><strong>损失赔偿</strong>：违约金不足以弥补损失的，可另行主张</li></ul><p>参考：《民法典》第 577 条、第 584 条、第 585 条</p>` },
  { id: 4, title: '政府采购评分标准设计原则', category: '评分标准', tags: ['评分', '评标', '权重'],
    content: `<p>评分标准应遵循以下原则：</p><ul><li><strong>客观量化</strong>：避免主观判断，每项指标有明确计分规则</li><li><strong>价格分</strong>：通常占 30%-60%，采用低价优先法计算</li><li><strong>技术分</strong>：占 30%-50%，评估技术方案、参数响应度</li><li><strong>商务分</strong>：占 10%-20%，评估资质、业绩、售后服务</li><li><strong>禁止设置</strong>：不得以特定区域业绩、特定品牌等排斥潜在供应商</li></ul>` },
  { id: 5, title: '限制性条款的识别与规避', category: '风险防控', tags: ['合规', '限制', '风险'],
    content: `<p><strong>常见限制性条款：</strong></p><ul><li>指定品牌、型号、产地（排斥竞争）</li><li>要求特定区域业绩（地域歧视）</li><li>过高资质要求（与项目规模不匹配）</li><li>不合理的交付周期（变相排斥）</li></ul><p><strong>规避建议：</strong>使用性能指标代替品牌、允许同等及以上产品、合理设置资质等级</p>` },
  { id: 6, title: '政府采购法中须知的采购方式', category: '法规解读', tags: ['法规', '采购方式'],
    content: `<p>根据《政府采购法》，主要采购方式：</p><ul><li><strong>公开招标</strong>：主要方式，适用于大多数项目</li><li><strong>邀请招标</strong>：特殊情形，向三家以上特定供应商发出邀请</li><li><strong>竞争性谈判</strong>：技术复杂或紧急情况</li><li><strong>询价</strong>：规格统一、现货充足的小额采购</li><li><strong>单一来源</strong>：只能从唯一供应商处采购的特殊情形</li></ul>` },
  { id: 7, title: '履约保证金与质量保证金区别', category: '术语解释', tags: ['保证金', '履约', '质量'],
    content: `<p><strong>履约保证金</strong>：合同签订前缴纳，保证按约履行，通常为合同金额 5%-10%，验收合格后退还。</p><p><strong>质量保证金</strong>：验收后留存部分款项作为质保担保，质保期满后退还，通常为合同金额 3%-5%。</p><p>两者可并存，但合计比例不宜过高。</p>` },
  { id: 8, title: '信息化项目采购特殊注意事项', category: '招标流程', tags: ['信息化', '软件', '数据安全'],
    content: `<p>信息化采购需额外关注：</p><ul><li><strong>数据安全</strong>：要求供应商通过等保认证、签订数据保密协议</li><li><strong>知识产权</strong>：明确源代码归属、使用权范围</li><li><strong>运维服务</strong>：SLA 约定（响应时间、解决时间）</li><li><strong>兼容性</strong>：与现有系统的集成要求</li><li><strong>培训</strong>：用户培训计划和交付物</li></ul>` },
])

const filtered = computed(() => {
  let list = items.value
  if (activeCat.value !== '全部') list = list.filter(i => i.category === activeCat.value)
  if (search.value.trim()) {
    const q = search.value.toLowerCase()
    list = list.filter(i => i.title.toLowerCase().includes(q) || i.content.toLowerCase().includes(q))
  }
  return list
})

const displayed = computed(() => filtered.value.map(i => ({ ...i, open: openMap.value[i.id] || false })))

function toggleItem(item) { openMap.value[item.id] = !openMap.value[item.id] }

function renderContent(item) {
  return item.content.replace(/\n/g, '')
}

function doSearch() {}
</script>

<style scoped>
.kb { max-width: 900px; margin: 0 auto; }
.page-title { font-size: 28px; font-weight: 700; letter-spacing: -0.8px; margin-bottom: 20px; }
.grad{background:linear-gradient(135deg,var(--accent),#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent}

.kb-search { display: flex; align-items: center; gap: 10px; padding: 12px 16px; background: var(--bg-card); border: 0.5px solid var(--border); border-radius: var(--radius-lg); margin-bottom: 16px; color: var(--text-tertiary); }
.kb-input { flex: 1; border: none; outline: none; font-size: 15px; font-family: var(--font); background: transparent; color: var(--text); }
.kb-input::placeholder { color: var(--text-tertiary); }

.kb-cats { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.cat-chip { padding: 7px 16px; border-radius: 100px; border: 0.5px solid var(--border); background: transparent; color: var(--text-secondary); font-size: 13px; cursor: pointer; transition: all var(--ease); font-family: var(--font); }
.cat-chip.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.cat-chip:hover:not(.active) { border-color: var(--accent); color: var(--accent); }

.kb-list { display: flex; flex-direction: column; gap: 10px; }
.kb-card { padding: 18px 22px; cursor: pointer; transition: all var(--ease); }
.kb-card:hover { transform: translateY(-1px); box-shadow: var(--shadow-md); }
.kb-cat-tag { font-size: 11px; font-weight: 550; color: var(--accent); text-transform: uppercase; letter-spacing: 0.5px; }
.kb-card h4 { font-size: 15px; font-weight: 600; margin-top: 6px; color: var(--text); }

.kb-body { margin-top: 14px; padding-top: 14px; border-top: 0.5px solid var(--border); }
.kb-content { font-size: 14px; line-height: 1.8; color: var(--text-secondary); }
.kb-content :deep(p) { margin-bottom: 10px; }
.kb-content :deep(ul), .kb-content :deep(ol) { padding-left: 20px; margin-bottom: 10px; }
.kb-content :deep(li) { margin-bottom: 4px; }
.kb-content :deep(strong) { color: var(--text); }
.kb-tags { display: flex; gap: 6px; margin-top: 12px; }
.kb-tag { font-size: 11px; color: var(--accent); }

.empty { text-align: center; padding: 40px; color: var(--text-tertiary); font-size: 14px; }

.expand-enter-active { transition: all 0.3s ease-out; overflow: hidden; }
.expand-leave-active { transition: all 0.2s ease-in; overflow: hidden; }
.expand-enter-from, .expand-leave-to { opacity: 0; max-height: 0; }
.expand-enter-to, .expand-leave-from { opacity: 1; max-height: 600px; }
</style>
