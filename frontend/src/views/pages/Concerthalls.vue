<script setup>
import { ref, onMounted } from 'vue';
import { ApiService } from '@/services/api';
import { useToast } from 'primevue/usetoast';
import { FilterMatchMode } from '@primevue/core/api';

const toast = useToast();

const concertHalls = ref([]);
const loading = ref(false);

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});

const loadConcertHalls = async () => {
    loading.value = true;
    try {
        const response = await ApiService.get('/concerthalls/');
        concertHalls.value = response.data;
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load concert halls', life: 3000 });
    } finally {
        loading.value = false;
    }
};

onMounted(loadConcertHalls);
</script>

<template>
  <div class="card">
    <h2 class="text-2xl font-bold mb-4">Concert Halls</h2>

    <div class="flex justify-end mb-4">
      <IconField>
        <InputIcon>
          <i class="pi pi-search" />
        </InputIcon>
        <InputText v-model="filters['global'].value" placeholder="Search concert halls..." />
      </IconField>
    </div>

    <DataTable
      :value="concertHalls"
      :filters="filters"
      :loading="loading"
      paginator
      :rows="5"
      :rowsPerPageOptions="[5, 10, 20]"
      tableStyle="min-width: 60rem"
      showGridlines
      :globalFilterFields="[
          'name',
          'city',
          'state',
          'country',
          'postal_code',
          'address',
          'capacity'
      ]"
      removableSort
    >
      <template #empty> No concert halls found. </template>

      <Column field="id" header="ID" sortable />
      <Column field="name" header="Name" sortable />
      
      <Column header="Image">
        <template #body="{ data }">
          <div v-if="data.image_url">
            <img 
              :src="data.image_url" 
              alt="Concert Hall Image" 
              class="w-16 h-16 object-cover rounded" 
            />
          </div>
        </template>
      </Column>

      <Column field="capacity" header="Capacity" sortable />
      <Column field="city" header="City" sortable />
      <Column field="state" header="State" sortable />
      <Column field="country" header="Country" sortable />
      <Column field="postal_code" header="Postal Code" sortable />
      <Column field="address" header="Address" sortable />
    </DataTable>
  </div>
</template>
