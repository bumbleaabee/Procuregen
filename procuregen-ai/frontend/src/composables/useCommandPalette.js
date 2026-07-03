/**
 * Ctrl+K 命令面板 composable
 */
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const visible = ref(false)
const query = ref('')

const commands = [
  { label: '新建采购文件', shortcut: 'Ctrl+N', action: (router) => router.push('/generate') },
  { label: '查看历史记录', shortcut: 'Ctrl+H', action: (router) => router.push('/history') },
  { label: '模板管理', shortcut: 'Ctrl+T', action: (router) => router.push('/templates') },
  { label: '回到首页', shortcut: 'Ctrl+Home', action: (router) => router.push('/') },
  { label: '切换暗色模式', shortcut: 'Ctrl+D', action: (_, toggleTheme) => toggleTheme?.() },
]

export function useCommandPalette() {
  const router = useRouter()

  function open() { visible.value = true; query.value = '' }
  function close() { visible.value = false }
  function toggle() { visible.value = !visible.value }

  const filtered = computed(() => {
    if (!query.value) return commands
    const q = query.value.toLowerCase()
    return commands.filter(c => c.label.toLowerCase().includes(q))
  })

  function execute(cmd) {
    visible.value = false
    cmd.action?.(router)
  }

  return { visible, query, filtered, open, close, toggle, execute, commands }
}

import { computed } from 'vue'
