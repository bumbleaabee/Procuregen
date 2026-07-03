/**
 * Scroll-triggered fade-in-up animation
 * Usage: <div v-fade-up>content</div>
 */
export const vFadeUp = {
  mounted(el) {
    el.classList.add('fade-up')
    const obs = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        el.classList.add('visible')
        obs.unobserve(el)
      }
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' })
    obs.observe(el)
    el._fadeObs = obs
  },
  unmounted(el) {
    el._fadeObs?.disconnect()
  }
}
