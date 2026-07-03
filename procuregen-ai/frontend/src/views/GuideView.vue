<template>
  <div class="guide-root">
    <h2 class="g-title">采购流程导览</h2>
    <p class="g-sub">点击每个步骤查看详细说明与专业建议</p>

    <div class="timeline">
      <div v-for="(step, i) in steps" :key="i" class="tl-item" :class="{ open: step.open, last: i === steps.length - 1 }">
        <div class="tl-marker" @click="toggle(i)">
          <div class="tl-dot" :class="{ done: i < current }">
            <svg v-if="i < current" width="14" height="14" viewBox="0 0 24 24" fill="none"><polyline points="20 6 9 17 4 12" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span v-else>{{ i + 1 }}</span>
          </div>
          <div v-if="!step.last" class="tl-line" :class="{ filled: i < current }"></div>
        </div>

        <div class="tl-card" :class="{ done: i < current }" @click="toggle(i)">
          <div class="tl-header">
            <span class="tl-num">Step {{ i + 1 }}</span>
            <h3>{{ step.title }}</h3>
            <span v-if="i < current" class="tl-check">✓</span>
          </div>
          <p class="tl-brief">{{ step.brief }}</p>

          <Transition name="slide">
            <div v-if="step.open" class="tl-detail">
              <div class="tl-section">
                <h4>📋 操作要点</h4>
                <ul><li v-for="p in step.points" :key="p">{{ p }}</li></ul>
              </div>
              <div class="tl-section">
                <h4>⚠️ 常见误区</h4>
                <ul><li v-for="m in step.mistakes" :key="m">{{ m }}</li></ul>
              </div>
              <div class="tl-section">
                <h4>💡 专业建议</h4>
                <p>{{ step.tip }}</p>
              </div>
              <div v-if="i < steps.length - 1" class="tl-next">
                <button class="apple-btn apple-btn-primary" @click.stop="nextStep(i)">继续：{{ steps[i+1].title }} →</button>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const current = ref(0)

const steps = reactive([
  { title: '需求调研与分析', brief: '明确采购目标、预算范围、技术规格和交付要求', open: true,
    points: ['与使用部门确认详细需求', '进行市场调研了解供应商情况', '编制采购需求说明书', '确定采购预算和资金来源'],
    mistakes: ['需求描述过于笼统', '技术参数照搬某一品牌', '未考虑后续运维成本'],
    tip: '需求阶段投入充分时间，需求越清晰后续越顺利。建议组织需求评审会。' },
  { title: '编制招标文件', brief: '按照规范格式编制完整的招标文件', open: false,
    points: ['编写采购公告和供应商须知', '制定详细的技术规格书', '设计合理的评分标准', '起草合同主要条款', '准备投标文件格式模板'],
    mistakes: ['评分标准主观性过强', '遗漏关键合同条款', '技术参数存在排他性'],
    tip: '评分标准应量化可衡量，价格分30%-60%为宜，技术分应有明确的评分细则。' },
  { title: '发布招标公告', brief: '在指定平台发布公告并接受供应商报名', open: false,
    points: ['选择合规的发布平台', '确保公告期不少于法定时限', '准备资格预审文件', '建立供应商答疑渠道'],
    mistakes: ['公告期不足20日', '资格条件设置过高', '答疑不及时不透明'],
    tip: '建议设立专门的答疑邮箱并定期汇总发布答疑公告，确保公平透明。' },
  { title: '开标评标', brief: '组织开标会议并进行专业评标', open: false,
    points: ['按规定时间地点开标', '组建专业评标委员会', '按评分标准逐项打分', '编制评标报告'],
    mistakes: ['评标委员会组成不合规', '评分过程缺乏记录', '忽视异常低价的合理性审查'],
    tip: '评标过程全程记录，每项评分应有书面依据。异常低价需要求供应商书面说明。' },
  { title: '定标与签约', brief: '确定中标人并签订采购合同', open: false,
    points: ['公示中标结果', '发出中标通知书', '签订正式采购合同', '收取履约保证金'],
    mistakes: ['公示期不足', '合同条款与招标文件不一致', '忽略履约保证金'],
    tip: '合同内容应与招标文件保持一致，重大变更需双方协商确认并记录。' },
  { title: '履约验收', brief: '监督合同执行并组织验收', open: false,
    points: ['跟踪交付进度', '组织到货或服务验收', '出具验收报告', '办理付款和保证金退还'],
    mistakes: ['验收标准不明确', '验收走过场', '付款与验收脱节'],
    tip: '严格按照合同约定的验收标准和流程执行，验收合格后及时出具书面报告。' },
])

function toggle(i) { steps[i].open = !steps[i].open; if (steps[i].open) current.value = Math.max(current.value, i) }

function nextStep(i) {
  steps[i].open = false
  const next = steps[i + 1]
  if (next) { next.open = true; current.value = Math.max(current.value, i + 1) }
}
</script>

<style scoped>
.guide-root { max-width: 760px; margin: 0 auto; }
.g-title { font-size: 26px; font-weight: 700; letter-spacing: -0.8px; margin-bottom: 4px; }
.g-sub { font-size: 14px; color: var(--text-secondary); margin-bottom: 32px; }

.timeline { position: relative; padding-left: 44px; }
.tl-item { position: relative; padding-bottom: 24px; }
.tl-item.last { padding-bottom: 0; }

.tl-marker { position: absolute; left: -44px; top: 0; width: 28px; display: flex; flex-direction: column; align-items: center; cursor: pointer; }
.tl-dot {
  width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  background: var(--border); color: var(--text-tertiary); font-size: 12px; font-weight: 650;
  transition: all var(--transition); z-index: 1; flex-shrink: 0;
}
.tl-dot.done { background: var(--accent); color: #fff; }
.tl-line { width: 2px; flex: 1; min-height: 40px; background: var(--border); margin: 4px 0; transition: background var(--transition); }
.tl-line.filled { background: var(--accent); }

.tl-card {
  background: var(--bg-card); border: 0.5px solid var(--border); border-radius: var(--radius-lg);
  padding: 20px 24px; cursor: pointer; transition: all var(--transition);
}
.tl-card:hover { border-color: var(--accent); box-shadow: var(--shadow-md); }
.tl-card.done { border-left: 3px solid var(--accent); }

.tl-header { display: flex; align-items: center; gap: 10px; }
.tl-num { font-size: 11px; font-weight: 600; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; }
.tl-header h3 { font-size: 16px; font-weight: 650; color: var(--text-primary); }
.tl-check { margin-left: auto; color: #34c759; font-weight: 700; }
.tl-brief { font-size: 14px; color: var(--text-secondary); margin-top: 8px; line-height: 1.6; }

.tl-detail { margin-top: 18px; padding-top: 18px; border-top: 0.5px solid var(--border); }
.tl-section { margin-bottom: 16px; }
.tl-section h4 { font-size: 13px; font-weight: 600; color: var(--text-primary); margin-bottom: 8px; }
.tl-section ul { padding-left: 18px; }
.tl-section li { font-size: 13px; color: var(--text-secondary); line-height: 1.7; margin-bottom: 4px; }
.tl-section p { font-size: 13px; color: var(--text-secondary); line-height: 1.7; }
.tl-next { margin-top: 12px; text-align: right; }

.slide-enter-active { transition: all 0.35s ease-out; }
.slide-leave-active { transition: all 0.25s ease-in; }
.slide-enter-from, .slide-leave-to { opacity: 0; max-height: 0; overflow: hidden; }
.slide-enter-to, .slide-leave-from { opacity: 1; max-height: 600px; }
</style>
