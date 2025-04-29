<script setup>
import { ref, onMounted } from 'vue';
import { FilterMatchMode } from '@primevue/core/api';
import { useConfirm } from 'primevue/useconfirm';
import { useToast } from 'primevue/usetoast';
import { ApiService } from '@/services/api';

const confirm = useConfirm();
const toast = useToast();

const tracks = ref([]);
const artists = ref({});
const selectedTracks = ref([]);
const loading = ref(false);

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});

const loadTracks = async () => {
  loading.value = true;
  try {
    const [tracksResponse, artistsResponse] = await Promise.all([
      ApiService.get('/tracks/'),
      ApiService.get('/artists/')
    ]);

    artists.value = artistsResponse.data.reduce((acc, artist) => {
      acc[artist.id] = artist.name;
      return acc;
    }, {});

    tracks.value = tracksResponse.data.map(track => ({
      ...track,
      artist_name: artists.value[track.artist] || 'Unknown Artist'
    }));

  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load tracks or artists', life: 3000 });
  } finally {
    loading.value = false;
  }
};

onMounted(loadTracks);

const deleteTracks = () => {
  confirm.require({
    message: selectedTracks.value.length > 1
      ? 'Do you want to delete these tracks?'
      : 'Do you want to delete this track?',
    header: 'Confirmation',
    rejectLabel: 'Cancel',
    acceptLabel: 'Delete',
    rejectProps: { severity: 'secondary', outlined: true },
    acceptProps: { severity: 'danger' },
    accept: async () => {
      const promises = selectedTracks.value.map(track =>
        ApiService.delete(`/tracks/${track.id}/`)
      );
      await Promise.all(promises);
      toast.add({ severity: 'success', summary: 'Deleted', detail: 'Track(s) deleted', life: 3000 });
      await loadTracks();
      selectedTracks.value = [];
    }
  });
};
</script>

<template>
  <div class="card">
    <h2 class="text-2xl font-bold mb-4">Tracks</h2>

    <DataTable
      v-model:filters="filters"
      v-model:selection="selectedTracks"
      :value="tracks"
      :loading="loading"
      showGridlines
      removableSort
      paginator
      :rows="5"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      tableStyle="min-width: 60rem"
      :globalFilterFields="['title', 'artist_name', 'release_date', 'current_rank', 'streams']"
    >
      <template #header>
        <div class="flex justify-between items-center">
          <div class="flex gap-2">
            <Button
              @click="deleteTracks"
              label="Delete"
              severity="danger"
              :disabled="!selectedTracks || selectedTracks.length < 1"
            />
          </div>
          <IconField>
            <InputIcon>
              <i class="pi pi-search" />
            </InputIcon>
            <InputText v-model="filters['global'].value" placeholder="Search tracks..." />
          </IconField>
        </div>
      </template>

      <Column selectionMode="multiple" headerStyle="width: 3rem" />
      <Column field="id" header="ID" sortable />
      <Column field="title" header="Title" sortable />
      <Column field="artist_name" header="Artist Name" sortable />
      <Column field="release_date" header="Release Date" sortable />
      <Column field="entry_date" header="Entry Date" sortable />
      <Column field="current_rank" header="Current Rank" sortable />
      <Column field="peak_rank" header="Peak Rank" sortable />
      <Column field="appearances" header="Appearances" sortable />
      <Column field="streams" header="Streams" sortable />
    </DataTable>
  </div>
</template>
