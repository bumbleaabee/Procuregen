<template>
  <div ref="card" class="tilt-card" :style="style">
    <div class="tilt-glow" :style="glowStyle"></div>
    <div class="tilt-content">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const card = ref(null)
const rotX = ref(0)
const rotY = ref(0)
const glowX = ref(50)
const glowY = ref(50)

const style = computed(() => ({
  transform: `perspective(1000px) rotateX(${rotX.value}deg) rotateY(${rotY.value}deg) scale3d(1.02,1.02,1.02)`,
}))

const glowStyle = computed(() => ({
  background: `radial-gradient(circle at ${glowX.value}% ${glowY.value}%, var(--accent-ghost) 0%, transparent 60%)`,
}))

function onMove(e) {
  const rect = card.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  const cx = rect.width / 2, cy = rect.height / 2
  rotX.value = ((y - cy) / cy) * -8
  rotY.value = ((x - cx) / cx) * 8
  glowX.value = (x / rect.width) * 100
  glowY.value = (y / rect.height) * 100
}

function onLeave() {
  rotX.value = 0; rotY.value = 0
  glowX.value = 50; glowY.value = 50
}

defineExpose({ onMove, onLeave })
</script>

<style scoped>
.tilt-card {
  position: relative;
  transition: transform 0.6s cubic-bezier(0.23, 1, 0.32, 1), box-shadow 0.6s ease;
  transform-style: preserve-3d;
  border-radius: inherit;
}
.tilt-glow {
  position: absolute; inset: 0; border-radius: inherit;
  opacity: 0; transition: opacity 0.4s ease; pointer-events: none; z-index: 0;
}
.tilt-card:hover .tilt-glow { opacity: 1; }
.tilt-content { position: relative; z-index: 1; border-radius: inherit; }
</style>
