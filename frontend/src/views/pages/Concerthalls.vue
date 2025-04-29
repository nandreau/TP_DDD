<script setup>
import { ref, onMounted, computed } from 'vue';
import { ApiService } from '@/services/api';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import { FilterMatchMode } from '@primevue/core/api';

const toast = useToast();
const confirm = useConfirm();

const concertHalls = ref([]);
const loading = ref(false);

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});

const selectedConcertHalls = ref([]);
const visibleAdd = ref(false);
const visibleUpdate = ref(false);

const formConcertHall = ref({
  concert_hall_id: '',
  name: '',
  capacity: 0,
  city: '',
  state: '',
  country: '',
  country_code: '',
  postal_code: '',
  address: '',
  latitude: 0,
  longitude: 0,
  image_url: ''
});

const user = JSON.parse(localStorage.getItem('userProfile'));
const isAdmin = computed(() => user?.role === 'admin');

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

const openUpdateDialog = () => {
  if (selectedConcertHalls.value.length === 1) {
    formConcertHall.value = { ...selectedConcertHalls.value[0] };
    visibleUpdate.value = true;
  }
};

const saveConcertHallUpdate = async () => {
  try {
    await ApiService.put(`/admin/concerthalls/${formConcertHall.value.id}/`, formConcertHall.value);
    toast.add({ severity: 'success', summary: 'Success', detail: 'Concert Hall updated', life: 3000 });
    visibleUpdate.value = false;
    await loadConcertHalls();
    selectedConcertHalls.value = [];
  } catch (error) {
    console.error(error);
  }
};

const deleteConcertHalls = () => {
  confirm.require({
    message: selectedConcertHalls.value.length > 1
      ? 'Do you want to delete these concert halls?'
      : 'Do you want to delete this concert hall?',
    header: 'Confirmation',
    rejectLabel: 'Cancel',
    acceptLabel: 'Delete',
    rejectProps: { severity: 'secondary', outlined: true },
    acceptProps: { severity: 'danger' },
    accept: async () => {
      try {
        const promises = selectedConcertHalls.value.map(hall =>
          ApiService.delete(`/admin/concerthalls/${hall.id}/`)
        );
        await Promise.all(promises);
        toast.add({ severity: 'success', summary: 'Deleted', detail: 'Concert Hall(s) deleted', life: 3000 });
        await loadConcertHalls();
        selectedConcertHalls.value = [];
      } catch (error) {
        console.error(error);
      }
    }
  });
};

onMounted(loadConcertHalls);
</script>

<template>
  <div class="card">
    <h2 class="text-2xl font-bold mb-4">Concert Halls</h2>

    <DataTable
      v-model:filters="filters"
      v-model:selection="selectedConcertHalls"
      :value="concertHalls"
      :loading="loading"
      paginator
      :rows="5"
      :rowsPerPageOptions="[5, 10, 20]"
      tableStyle="min-width: 60rem"
      showGridlines
      selectionMode="multiple"
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
      <template #header>
        <div class="flex justify-between items-center">
          <div v-if="isAdmin" class="flex gap-2">
            <Button @click="openUpdateDialog" label="Update" :disabled="!selectedConcertHalls.length" severity="warn" />
            <Button @click="deleteConcertHalls" label="Delete" :disabled="!selectedConcertHalls.length" severity="danger" />
          </div>
          <IconField>
            <InputIcon>
              <i class="pi pi-search" />
            </InputIcon>
            <InputText v-model="filters['global'].value" placeholder="Search concert halls..." />
          </IconField>
        </div>
      </template>

      <template #empty> No concert halls found. </template>

      <Column v-if="isAdmin" selectionMode="multiple" headerStyle="width: 3rem" />
      <Column field="id" header="ID" sortable />
      <Column field="name" header="Name" sortable />
      
      <Column header="Image">
        <template #body="{ data }">
          <div v-if="data.image_url">
            <img :src="data.image_url" alt="Concert Hall Image" class="w-16 h-16 object-cover rounded" />
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

  <Dialog v-model:visible="visibleUpdate" modal header="Update Concert Hall" :style="{ width: '30rem' }">
    <div class="flex flex-col gap-4">
      <InputText v-model="formConcertHall.concert_hall_id" placeholder="Concert Hall ID" disabled />
      <InputText v-model="formConcertHall.name" placeholder="Name" />
      <InputText v-model="formConcertHall.capacity" type="number" placeholder="Capacity" />
      <InputText v-model="formConcertHall.city" placeholder="City" />
      <InputText v-model="formConcertHall.state" placeholder="State" />
      <InputText v-model="formConcertHall.country" placeholder="Country" />
      <InputText v-model="formConcertHall.country_code" placeholder="Country Code" />
      <InputText v-model="formConcertHall.postal_code" placeholder="Postal Code" />
      <InputText v-model="formConcertHall.address" placeholder="Address" />
      <InputText v-model="formConcertHall.latitude" type="number" placeholder="Latitude" />
      <InputText v-model="formConcertHall.longitude" type="number" placeholder="Longitude" />
      <InputText v-model="formConcertHall.image_url" placeholder="Image URL" />

      <div class="flex justify-end gap-2">
        <Button label="Cancel" severity="secondary" @click="visibleUpdate = false" outlined />
        <Button label="Save" @click="saveConcertHallUpdate" />
      </div>
    </div>
  </Dialog>
</template>
