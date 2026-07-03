<template>
  <canvas ref="canvas" class="particle-canvas"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let ctx, w, h, particles = [], mouse = { x: 0, y: 0 }, animId

class Particle {
  constructor() {
    this.reset()
    this.y = Math.random() * h
  }
  reset() {
    this.x = Math.random() * w
    this.y = -10
    this.size = Math.random() * 2 + 0.5
    this.speed = Math.random() * 0.5 + 0.2
    this.opacity = Math.random() * 0.5 + 0.15
    this.drift = (Math.random() - 0.5) * 0.3
  }
  update() {
    this.y += this.speed
    this.x += this.drift + (mouse.x - w/2) * 0.0001
    if (this.y > h + 10) this.reset()
  }
  draw() {
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
    ctx.fillStyle = `rgba(${isDark ? '255,255,255' : '0,113,227'},${this.opacity})`
    ctx.fill()
  }
}

let isDark = false

function init() {
  w = canvas.value.width = window.innerWidth
  h = canvas.value.height = window.innerHeight
  ctx = canvas.value.getContext('2d')
  particles = Array.from({ length: 80 }, () => new Particle())
}

function animate() {
  ctx.clearRect(0, 0, w, h)
  // 连线
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x
      const dy = particles[i].y - particles[j].y
      const dist = Math.sqrt(dx * dx + dy * dy)
      if (dist < 120) {
        ctx.beginPath()
        ctx.moveTo(particles[i].x, particles[i].y)
        ctx.lineTo(particles[j].x, particles[j].y)
        ctx.strokeStyle = `rgba(${isDark ? '255,255,255' : '0,113,227'},${0.04 * (1 - dist/120)})`
        ctx.lineWidth = 0.5
        ctx.stroke()
      }
    }
  }
  particles.forEach(p => { p.update(); p.draw() })
  animId = requestAnimationFrame(animate)
}

function onMouse(e) { mouse.x = e.clientX; mouse.y = e.clientY }
function onResize() { w = canvas.value.width = innerWidth; h = canvas.value.height = innerHeight }
function onTheme() { isDark = document.documentElement.classList.contains('dark') }

onMounted(() => {
  isDark = document.documentElement.classList.contains('dark')
  init(); animate()
  window.addEventListener('mousemove', onMouse)
  window.addEventListener('resize', onResize)
  new MutationObserver(onTheme).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })
})
onUnmounted(() => {
  cancelAnimationFrame(animId)
  window.removeEventListener('mousemove', onMouse)
  window.removeEventListener('resize', onResize)
})
</script>

<style scoped>
.particle-canvas {
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
}
</style>
