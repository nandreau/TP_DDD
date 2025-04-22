<template>
    <ConfirmDialog></ConfirmDialog>
    <Toast />
    <router-view />
</template>

<script setup>
import { initToast } from '@/composables/usePrimeToast'

initToast()
</script>
  