<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import HeaderComponent from '../../components/HeaderComponent.vue'

const visible = ref(false)

const updateVisibility = () => {
  visible.value = window.innerWidth > 991
}

onMounted(() => {
  updateVisibility()
  window.addEventListener('resize', updateVisibility)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateVisibility)
})
</script>

<template>
    <div :class="['main-container', { 'sidebar-hidden': !visible }]">
      <HeaderComponent v-model:visible="visible" />
      <div class="layout-main-container">
        <router-view />
      </div>
    </div>
</template>
