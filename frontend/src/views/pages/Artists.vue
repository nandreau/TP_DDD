<script setup>
import { ref, onMounted, computed } from 'vue';
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import { ApiService } from '@/services/api';

const toast = useToast();
const confirm = useConfirm();

const artists = ref([]);
const loading = ref(false);

const genres = ref({});
const genreFamilies = ref({});

const genreOptions = computed(() => {
    return Object.entries(genres.value).map(([id, name]) => ({
        label: name,
        value: parseInt(id)
    }));
});

const genreFamilyOptions = computed(() => {
    return Object.entries(genreFamilies.value).map(([id, name]) => ({
        label: name,
        value: parseInt(id)
    }));
});


const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});

const selectedArtists = ref([]);
const visibleAdd = ref(false);
const visibleUpdate = ref(false);
const formArtist = ref({
    name: '',
    spotify_popularity: 0,
    followers: 0,
    longevity: 0,
    top_chart_presence: 0,
    spotify_streams_total: 0,
    stats_FR: 0,
    stats_GB: 0,
    stats_DE: 0,
    stats_IT: 0,
    stats_ES: 0,
    stats_BE: 0,
    genre: null,
    genre_family: null
});

// 💬 Get user from localStorage
const user = JSON.parse(localStorage.getItem('userProfile'));
const isAdmin = computed(() => user?.role === 'admin');

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

const openAddDialog = () => {
    formArtist.value = {
        name: '',
        spotify_popularity: 0,
        followers: 0,
        longevity: 0,
        top_chart_presence: 0,
        spotify_streams_total: 0,
        stats_FR: 0,
        stats_GB: 0,
        stats_DE: 0,
        stats_IT: 0,
        stats_ES: 0,
        stats_BE: 0,
        genre: null,
        genre_family: null
    };
    visibleAdd.value = true;
};

const saveNewArtist = async () => {
    await ApiService.post('/admin/artists/', formArtist.value);
    toast.add({ severity: 'success', summary: 'Success', detail: 'Artist created', life: 3000 });
    visibleAdd.value = false;
    await loadArtists();
};

const openUpdateDialog = () => {
    if (selectedArtists.value.length === 1) {
        const selected = selectedArtists.value[0];
        formArtist.value = {
            id: selected.id,
            name: selected.name,
            spotify_popularity: selected.spotify_popularity,
            followers: selected.followers,
            longevity: selected.longevity,
            top_chart_presence: selected.top_chart_presence,
            spotify_streams_total: selected.spotify_streams_total,
            stats_FR: selected.stats_FR,
            stats_GB: selected.stats_GB,
            stats_DE: selected.stats_DE,
            stats_IT: selected.stats_IT,
            stats_ES: selected.stats_ES,
            stats_BE: selected.stats_BE,
            genre: selected.genre,
            genre_family: selected.genre_family,
        };
        visibleUpdate.value = true;
    }
};


const saveArtistUpdate = async () => {
    const response = await ApiService.put(`/admin/artists/${formArtist.value.id}/`, formArtist.value);
    console.log(response)
    toast.add({ severity: 'success', summary: 'Success', detail: 'Artist updated', life: 3000 });
    visibleUpdate.value = false;
    await loadArtists();
    selectedArtists.value = [];
};

const deleteArtists = () => {
    confirm.require({
        message: selectedArtists.value.length > 1
            ? 'Do you want to delete these artists?'
            : 'Do you want to delete this artist?',
        header: 'Confirmation',
        rejectLabel: 'Cancel',
        acceptLabel: 'Delete',
        rejectProps: { severity: 'secondary', outlined: true },
        acceptProps: { severity: 'danger' },
        accept: async () => {
            const promises = selectedArtists.value.map(artist =>
                ApiService.delete(`/admin/artists/${artist.id}/`)
            );
            await Promise.all(promises);
            console.log(promises)
            toast.add({ severity: 'success', summary: 'Deleted', detail: 'Artist(s) deleted', life: 3000 });
            await loadArtists();
            selectedArtists.value = [];
        }
    });
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

        <DataTable
            v-model:filters="filters"
            v-model:selection="selectedArtists"
            :value="artists"
            :loading="loading"
            paginator
            :rows="5"
            :rowsPerPageOptions="[5, 10, 20]"
            showGridlines
            selectionMode="multiple"
            :globalFilterFields="[
                'name',
                'spotify_popularity',
                'followers',
                'spotify_streams_total',
                'genre_name',
                'genre_family_name'
            ]"
            removableSort
            tableStyle="min-width: 50rem"
        >

        <template #header>
                <div class="flex justify-between items-center">
                    <div v-if="isAdmin" class="flex gap-2">
                        <Button @click="openAddDialog" label="Add" />
                        <Button
                            @click="openUpdateDialog"
                            label="Update"
                            :disabled="!selectedArtists.length"
                            severity="warn"
                        />
                        <Button
                            @click="deleteArtists"
                            label="Delete"
                            :disabled="!selectedArtists.length"
                            severity="danger"
                        />
                    </div>
                    <IconField>
                        <InputIcon>
                            <i class="pi pi-search" />
                        </InputIcon>
                        <InputText v-model="filters['global'].value" placeholder="Search users..." />
                    </IconField>
                </div>
            </template>

            <template #empty> No artists found. </template>

            <Column  v-if="isAdmin" selectionMode="multiple" headerStyle="width: 3rem" />
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

    <Dialog v-model:visible="visibleAdd" modal header="Add New Artist" :style="{ width: '30rem' }">
        <div class="flex flex-col gap-4">
            <div class="flex flex-col gap-1">
                <label class="font-semibold">Name</label>
                <InputText v-model="formArtist.name" placeholder="Name" />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-semibold">Spotify Popularity</label>
                <InputText v-model="formArtist.spotify_popularity" type="number" placeholder="Popularity" />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-semibold">Followers</label>
                <InputText v-model="formArtist.followers" type="number" placeholder="Followers" />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-semibold">Spotify Streams Total</label>
                <InputText v-model="formArtist.spotify_streams_total" type="number" placeholder="Streams" />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-semibold">Genre</label>
                <Dropdown v-model="formArtist.genre" :options="genreOptions" optionLabel="label" optionValue="value" placeholder="Select Genre" class="w-full" />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-semibold">Genre Family</label>
                <Dropdown v-model="formArtist.genre_family" :options="genreFamilyOptions" optionLabel="label" optionValue="value" placeholder="Select Genre Family" class="w-full" />
            </div>

            <div class="flex justify-end gap-2">
                <Button label="Cancel" severity="secondary" @click="visibleAdd = false" outlined />
                <Button label="Save" @click="saveNewArtist" />
            </div>
        </div>
    </Dialog>

    <Dialog v-model:visible="visibleUpdate" modal header="Update Artist" :style="{ width: '30rem' }">
        <div class="flex flex-col gap-4">
            <div class="flex flex-col gap-1">
                <label class="font-semibold">Name</label>
                <InputText v-model="formArtist.name" placeholder="Name" />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-semibold">Spotify Popularity</label>
                <InputText v-model="formArtist.spotify_popularity" type="number" placeholder="Popularity" />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-semibold">Followers</label>
                <InputText v-model="formArtist.followers" type="number" placeholder="Followers" />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-semibold">Spotify Streams Total</label>
                <InputText v-model="formArtist.spotify_streams_total" type="number" placeholder="Streams" />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-semibold">Genre</label>
                <Dropdown v-model="formArtist.genre" :options="genreOptions" optionLabel="label" optionValue="value" placeholder="Select Genre" class="w-full" />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-semibold">Genre Family</label>
                <Dropdown v-model="formArtist.genre_family" :options="genreFamilyOptions" optionLabel="label" optionValue="value" placeholder="Select Genre Family" class="w-full" />
            </div>
            <div class="flex justify-end gap-2">
                <Button label="Cancel" severity="secondary" @click="visibleUpdate = false" outlined />
                <Button label="Save" @click="saveArtistUpdate" />
            </div>
        </div>
    </Dialog>
</template>
