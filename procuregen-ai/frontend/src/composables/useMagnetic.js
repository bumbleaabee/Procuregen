/**
 * 磁吸悬停 + 涟漪效果 composable
 */
export function magneticHover(el, strength = 0.3) {
  function onMove(e) {
    const rect = el.getBoundingClientRect()
    const x = (e.clientX - rect.left - rect.width / 2) * strength
    const y = (e.clientY - rect.top - rect.height / 2) * strength
    el.style.transform = `translate(${x}px, ${y}px)`
  }
  function onLeave() {
    el.style.transform = 'translate(0, 0)'
  }
  el.addEventListener('mousemove', onMove)
  el.addEventListener('mouseleave', onLeave)
  return () => {
    el.removeEventListener('mousemove', onMove)
    el.removeEventListener('mouseleave', onLeave)
  }
}
