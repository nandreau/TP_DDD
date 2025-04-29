<script setup>
import { ref, onMounted } from 'vue';
import { FilterMatchMode } from '@primevue/core/api';
import { useConfirm } from 'primevue/useconfirm';
import { useToast } from 'primevue/usetoast';
import { ApiService } from '@/services/api';

const confirm = useConfirm();
const toast = useToast();

const events = ref([]);
const concertHalls = ref({});
const selectedEvents = ref([]);
const loading = ref(false);

const visibleUpdate = ref(false);
const formEvent = ref({
    title: '',
    concert_hall: null,
    event_start: '',
    event_end: '',
    image_url: ''
});
const selectedEventId = ref(null);

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});

const loadEvents = async () => {
  loading.value = true;
  try {
    const [eventsResponse, concertHallsResponse] = await Promise.all([
      ApiService.get('/events/'),
      ApiService.get('/concerthalls/')
    ]);

    concertHalls.value = concertHallsResponse.data.reduce((acc, hall) => {
      acc[hall.id] = hall.name;
      return acc;
    }, {});

    events.value = eventsResponse.data.map(event => ({
      ...event,
      concert_hall_name: concertHalls.value[event.concert_hall] || 'Unknown Hall',
      first_image: event.image_url ? event.image_url.split(',')[0].trim() : null
    }));

  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load events or concert halls', life: 3000 });
  } finally {
    loading.value = false;
  }
};

onMounted(loadEvents);

const deleteEvents = () => {
  confirm.require({
    message: selectedEvents.value.length > 1
      ? 'Do you want to delete these events?'
      : 'Do you want to delete this event?',
    header: 'Confirmation',
    rejectLabel: 'Cancel',
    acceptLabel: 'Delete',
    rejectProps: { severity: 'secondary', outlined: true },
    acceptProps: { severity: 'danger' },
    accept: async () => {
      const promises = selectedEvents.value.map(event =>
        ApiService.delete(`/admin/events/${event.id}/`)
      );
      await Promise.all(promises);
      toast.add({ severity: 'success', summary: 'Deleted', detail: 'Event(s) deleted', life: 3000 });
      await loadEvents();
      selectedEvents.value = [];
    }
  });
};

const openUpdateDialog = () => {
  if (selectedEvents.value.length === 1) {
    const selected = selectedEvents.value[0];
    selectedEventId.value = selected.id;
    formEvent.value = {
      title: selected.title,
      concert_hall: selected.concert_hall,
      event_start: selected.event_start,
      event_end: selected.event_end,
      image_url: selected.image_url
    };
    visibleUpdate.value = true;
  }
};

const saveEventUpdate = async () => {
    await ApiService.patch(`/events/organizer/${selectedEventId.value}/`, {
      title: formEvent.value.title,
      concert_hall: formEvent.value.concert_hall,
      event_start: formEvent.value.event_start,
      event_end: formEvent.value.event_end,
      image_url: formEvent.value.image_url
    });
    toast.add({ severity: 'success', summary: 'Success', detail: 'Event updated', life: 3000 });
    visibleUpdate.value = false;
    await loadEvents();
    selectedEvents.value = [];
};
</script>

<template>
  <div class="card">
    <h2 class="text-2xl font-bold mb-4">Events</h2>

    <DataTable
      v-model:filters="filters"
      v-model:selection="selectedEvents"
      :value="events"
      :loading="loading"
      showGridlines
      removableSort
      paginator
      :rows="5"
      :rowsPerPageOptions="[5, 10, 20]"
      tableStyle="min-width: 60rem"
      :globalFilterFields="['title', 'concert_hall_name', 'event_start', 'event_end']"
    >
      <template #header>
        <div class="flex justify-between items-center">
          <div class="flex gap-2">
            <Button @click="openUpdateDialog" label="Update" severity="warn" :disabled="!selectedEvents || selectedEvents.length !== 1" />
            <Button @click="deleteEvents" label="Delete" severity="danger" :disabled="!selectedEvents || selectedEvents.length < 1" />
          </div>
          <IconField>
            <InputIcon>
              <i class="pi pi-search" />
            </InputIcon>
            <InputText v-model="filters['global'].value" placeholder="Search events..." />
          </IconField>
        </div>
      </template>

      <Column selectionMode="multiple" headerStyle="width: 3rem" />
      <Column field="id" header="ID" sortable />
      <Column field="title" header="Title" sortable />
      <Column header="Image">
        <template #body="{ data }">
          <div v-if="data.first_image">
            <img
              :src="data.first_image"
              alt="Event Image"
              class="w-16 h-16 object-cover rounded"
            />
          </div>
        </template>
      </Column>
      <Column field="concert_hall_name" header="Concert Hall" sortable />
      <Column field="event_start" header="Start Date" sortable />
      <Column field="event_end" header="End Date" sortable />
    </DataTable>

    <!-- Update Dialog -->
    <Dialog v-model:visible="visibleUpdate" modal header="Update Event" :style="{ width: '30rem' }">
      <span class="text-surface-500 dark:text-surface-400 block mb-8">Update event information.</span>

      <div class="flex flex-col gap-4">
        <div class="flex items-center gap-4">
          <label for="title" class="font-semibold w-32">Title</label>
          <InputText id="title" class="flex-auto" v-model="formEvent.title" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4">
          <label for="concert_hall" class="font-semibold w-32">Concert Hall ID</label>
          <InputText id="concert_hall" class="flex-auto" v-model="formEvent.concert_hall" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4">
          <label for="event_start" class="font-semibold w-32">Start Date</label>
          <InputText id="event_start" class="flex-auto" v-model="formEvent.event_start" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4">
          <label for="event_end" class="font-semibold w-32">End Date</label>
          <InputText id="event_end" class="flex-auto" v-model="formEvent.event_end" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4">
          <label for="image_url" class="font-semibold w-32">Image URL</label>
          <InputText id="image_url" class="flex-auto" v-model="formEvent.image_url" autocomplete="off" />
        </div>
      </div>

      <div class="flex justify-end gap-2 mt-6">
        <Button type="button" label="Cancel" severity="secondary" @click="visibleUpdate = false" outlined />
        <Button type="button" label="Save" @click="saveEventUpdate" />
      </div>
    </Dialog>
  </div>
</template>
