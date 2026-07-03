<template>
  <div class="radar-chart" v-if="data.length">
    <svg :viewBox="`0 0 ${size} ${size}`" :width="size" :height="size">
      <!-- 背景网格 -->
      <polygon
        v-for="level in 5" :key="level"
        :points="gridPoints(level / 5)"
        fill="none" :stroke="borderColor" stroke-width="0.5"
      />
      <!-- 轴线 -->
      <line
        v-for="(_, i) in data" :key="'axis-'+i"
        :x1="cx" :y1="cy"
        :x2="cx + r * Math.cos(angle(i) - Math.PI/2)"
        :y2="cy + r * Math.sin(angle(i) - Math.PI/2)"
        :stroke="borderColor" stroke-width="0.5"
      />
      <!-- 数据区域 -->
      <polygon :points="dataPoints" fill="var(--accent)" fill-opacity="0.15" stroke="var(--accent)" stroke-width="1.5" />
      <!-- 数据点 -->
      <circle
        v-for="(d, i) in data" :key="'dot-'+i"
        :cx="cx + (d.value / 100) * r * Math.cos(angle(i) - Math.PI/2)"
        :cy="cy + (d.value / 100) * r * Math.sin(angle(i) - Math.PI/2)"
        r="4" fill="var(--accent)" stroke="#fff" stroke-width="2"
      />
      <!-- 标签 -->
      <text
        v-for="(d, i) in data" :key="'label-'+i"
        :x="cx + (r + 24) * Math.cos(angle(i) - Math.PI/2)"
        :y="cy + (r + 24) * Math.sin(angle(i) - Math.PI/2)"
        text-anchor="middle" dominant-baseline="middle"
        fill="currentColor" font-size="11" font-weight="500"
      >{{ d.label }} {{ d.value }}%</text>
    </svg>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: { type: Array, default: () => [] },
  size: { type: Number, default: 260 },
})

const cx = computed(() => props.size / 2)
const cy = computed(() => props.size / 2)
const r = computed(() => props.size * 0.32)
const borderColor = 'var(--border)'

function angle(i) { return (2 * Math.PI * i) / props.data.length }
function gridPoints(scale) {
  return props.data.map((_, i) => {
    const x = cx.value + r.value * scale * Math.cos(angle(i) - Math.PI/2)
    const y = cy.value + r.value * scale * Math.sin(angle(i) - Math.PI/2)
    return `${x},${y}`
  }).join(' ')
}
const dataPoints = computed(() => {
  return props.data.map((d, i) => {
    const x = cx.value + (d.value / 100) * r.value * Math.cos(angle(i) - Math.PI/2)
    const y = cy.value + (d.value / 100) * r.value * Math.sin(angle(i) - Math.PI/2)
    return `${x},${y}`
  }).join(' ')
})
</script>

<style scoped>
.radar-chart { display: flex; justify-content: center; padding: 16px 0; color: var(--text-secondary); }
</style>
