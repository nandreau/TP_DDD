<template>
    <div :class="['main-container', { 'sidebar-hidden': !visible }]">
      <HeaderComponent v-model:visible="visible" />
      <div class="layout-main-container">
        <!-- Your page content here -->
      </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import HeaderComponent from './components/HeaderComponent.vue'

const visible = ref(false)
</script>
  