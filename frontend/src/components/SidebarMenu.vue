<template>
    <Drawer :visible="visible" @update:visible="onUpdateVisible">
      <template #container>
        <div class="flex flex-col h-full">
          <div class="flex items-center px-6 pt-4 gap-2">
            <svg class="max-h-14" fill="var(--primary-color)" viewBox="-4 -4 28 28">
              <path d="M15.75 8l-3.74-3.75a3.99 3.99 0 0 1 6.82-3.08A4 4 0 0 1 15.75 8zM1.85 15.3l9.2-9.19 2.83 2.83-9.2 9.2-2.82-2.84zM.45 18.13l2.11-2.12 1.42 1.42-2.12 2.12-1.42-1.42zM10 15l2-2v7h-2v-5z"/>
            </svg>
            <span class="font-semibold text-2xl text-primary">Concert App</span>
          </div>
  
          <ul class="layout-menu p-4">
            <template v-for="(section, i) in model" :key="i">
              <li class="mt-4 mb-2 font-medium text-sm text-gray-500 uppercase">{{ section.label }}</li>
              <template v-for="(item, j) in section.items" :key="j">
                <router-link
                  v-ripple
                  :to="item.to"
                  class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all cursor-pointer hover:bg-surface-100 dark:hover:bg-surface-800"
                  :class="{ 'text-primary font-semibold': isActive(item) }"
                >
                  <i :class="item.icon" class="text-base"></i>
                  <span>{{ item.label }}</span>
                </router-link>
              </template>
            </template>
          </ul>
        </div>
      </template>
    </Drawer>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import { useRoute } from 'vue-router';
  
  const props = defineProps({ visible: Boolean });
  const emit = defineEmits(['update:visible']);
  const route = useRoute();
  
  function onUpdateVisible(val) {
    emit('update:visible', val);
  }
  
  function isActive(item) {
    return route.path === item.to;
  }
  
  // Get current user
  const user = JSON.parse(localStorage.getItem('userProfile') || '{}');
  const role = user?.role || null;
  
  // Full menu model
  const fullMenu = [
    { label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/' },
    { label: 'Generate Event', icon: 'pi pi-fw pi-calendar-plus', to: '/Generate-event' },
    { label: 'Events', icon: 'pi pi-fw pi-calendar', to: '/Events' },
    { label: 'Admin', icon: 'pi pi-fw pi-user-edit', to: '/Admin' },
    { label: 'Artists', icon: 'pi pi-fw pi-star', to: '/Artists' },
    { label: 'Concert Halls', icon: 'pi pi-fw pi-building', to: '/Concerthalls' },
    { label: 'Tracks', icon: 'pi pi-fw pi-headphones', to: '/Tracks' }
  ];
  console.log(role)
  // Role-based filtering
  const filteredItems = computed(() => {
    if (role === 'admin') {
      return fullMenu;
    }
  
    if (role === 'artist') {
      return fullMenu.filter(item =>
        ['/', '/Concerthalls', '/Tracks'].includes(item.to)
      );
    }
    console.log(role)
    if (role === 'organizer') {
      return fullMenu.filter(item =>
        ['/', '/Generate-event', '/Events', '/Concerthalls', '/Artists', '/Tracks'].includes(item.to)
      );
    }
  
    return [];
  });
  
  const model = computed(() => [
    {
      label: 'Home',
      items: filteredItems.value
    }
  ]);

  </script>
  
  