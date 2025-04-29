<script setup>
import { ref, onMounted } from 'vue';
import { ApiService } from '@/services/api';
import { useToast } from 'primevue/usetoast';
import { FilterMatchMode } from '@primevue/core/api';

const toast = useToast();

const artists = ref([]);
const loading = ref(false);

const genres = ref({});
const genreFamilies = ref({});

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});

const loadArtists = async () => {
    loading.value = true;
    try {
        const [artistsResponse, genresResponse, genreFamiliesResponse] = await Promise.all([
            ApiService.get('/artists/'),
            ApiService.get('/genres/'),
            ApiService.get('/genrefamilies/')
        ]);

        genres.value = genresResponse.data.reduce((acc, genre) => {
            acc[genre.id] = genre.name;
            return acc;
        }, {});

        genreFamilies.value = genreFamiliesResponse.data.reduce((acc, family) => {
            acc[family.id] = family.name;
            return acc;
        }, {});

        artists.value = artistsResponse.data.map(artist => ({
            ...artist,
            genre_name: genres.value[artist.genre] || 'Unknown Genre',
            genre_family_name: genreFamilies.value[artist.genre_family] || 'Unknown Family'
        }));

    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load artists/genres/families', life: 3000 });
    } finally {
        loading.value = false;
    }
};


onMounted(loadArtists);

const getGenreName = (id) => {
    return genres.value[id] || 'Unknown Genre';
};

const getGenreFamilyName = (id) => {
    return genreFamilies.value[id] || 'Unknown Family';
};
</script>


<template>
    <div class="card">
        <h2 class="text-2xl font-bold mb-4">Artists</h2>

        <div class="flex justify-end mb-4">
        <IconField>
            <InputIcon>
            <i class="pi pi-search" />
            </InputIcon>
            <InputText v-model="filters['global'].value" placeholder="Search artists..." />
        </IconField>
        </div>

        <DataTable
        :value="artists"
        :filters="filters"
        :loading="loading"
        paginator
        :rows="5"
        :rowsPerPageOptions="[5, 10, 20]"
        tableStyle="min-width: 50rem"
        showGridlines
        :globalFilterFields="[
            'name',
            'spotify_popularity',
            'followers',
            'spotify_streams_total',
            'genre_name',
            'genre_family_name'
        ]"
        removableSort

        >
        <template #empty> No artists found. </template>

        <Column field="id" header="ID" sortable />
        <Column field="name" header="Name" sortable />
        <Column field="spotify_popularity" header="Popularity" sortable />
        <Column field="followers" header="Followers" sortable />
        <Column field="spotify_streams_total" header="Streams" sortable />

        <Column header="Genre" sortable>
            <template #body="{ data }">
            {{ getGenreName(data.genre) }}
            </template>
        </Column>

        <Column header="Genre Family" sortable>
            <template #body="{ data }">
            {{ getGenreFamilyName(data.genre_family) }}
            </template>
        </Column>
        </DataTable>
    </div>
</template>
