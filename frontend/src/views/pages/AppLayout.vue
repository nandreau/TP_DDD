<script setup>
import { ref, onMounted } from 'vue'
import HeaderComponent from '../../components/HeaderComponent.vue'

const visible = ref(false)

onMounted(() => {
  if (window.innerWidth > 991) {
    visible.value = true
  }
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
