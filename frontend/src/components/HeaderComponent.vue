<template>
  <!-- SidebarMenu in a Drawer -->
  <SidebarMenu v-model:visible="localVisible" />
  
  <header class="layout-topbar">
    <!-- Logo & Menu Button -->
    <div class="layout-topbar-logo-container">

      <!-- Button to open the sidebar -->
      <div class="lg:!hidden flex items-center">
        <button class="layout-menu-button layout-topbar-action" @click="toggleSidebar">
          <i class="pi pi-bars"></i>
        </button>
        <router-link to="/" class="layout-topbar-logo">
          <svg  fill="var(--primary-color)" viewBox="-4 -4 28 28"><path d="M15.75 8l-3.74-3.75a3.99 3.99 0 0 1 6.82-3.08A4 4 0 0 1 15.75 8zm-13.9 7.3l9.2-9.19 2.83 2.83-9.2 9.2-2.82-2.84zm-1.4 2.83l2.11-2.12 1.42 1.42-2.12 2.12-1.42-1.42zM10 15l2-2v7h-2v-5z"/></svg>
          <span>Concert App</span>
        </router-link>
      </div>
    </div>

    <!-- Topbar Actions -->
    <div class="layout-topbar-actions">
      <ul class="flex list-none m-0 p-0 gap-2 items-center">
        <ThemeSwitcher />
        <li>
          <button type="button"
              class="layout-topbar-action"
              @click="signOut">
              <i :class="`dark:text-white pi pi-power-off`" />
          </button>
        </li>
      </ul>
    </div>
  </header>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue'
import { useRouter } from 'vue-router'
import SidebarMenu from './SidebarMenu.vue'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const props = defineProps({
  visible: Boolean
})
const emit = defineEmits(['update:visible'])

const localVisible = ref(props.visible)
const router = useRouter()

watch(() => props.visible, val => {
  localVisible.value = val
})

watch(localVisible, val => {
  emit('update:visible', val)
})

const toggleSidebar = () => {
  emit('update:visible', !props.visible)
}

const signOut = () => {
  localStorage.removeItem('authToken')
  toast.add({
    severity: 'success',
    summary: 'Logged out',
    detail: 'You have been successfully logged out.',
    life: 3000
  })
  router.push('/login')
}
</script>

<style scoped>
</style>