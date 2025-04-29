<script setup>
import { ref, onMounted, watch } from 'vue';
import { ApiService } from '@/services/api';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import { FilterMatchMode } from '@primevue/core/api';
import { format } from 'date-fns'; // Add this if not already


const toast = useToast();
const confirm = useConfirm();

const countries = ref([]);
const concertHalls = ref([]);
const genreFamilies = ref([]);

const selectedCountry = ref(null);
const selectedConcertHall = ref(null);
const selectedGenreFamily = ref(null);

const eventStart = ref(new Date());
const castingSize = ref(2);
const qualityScore = ref(5);
const customTitle = ref('');

const loadingConcertHalls = ref(false);

const generatedEvent = ref(null);
const showValidationDialog = ref(false);

const loadCountries = async () => {
  try {
    const response = await ApiService.get('/countries/');
    countries.value = response.data;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load countries', life: 3000 });
  }
};

const loadGenreFamilies = async () => {
  try {
    const response = await ApiService.get('/genrefamilies/');
    genreFamilies.value = response.data.map(family => (family.name));
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load genre families', life: 3000 });
  }
};

const loadConcertHalls = async () => {
  if (!selectedCountry.value) return;
  loadingConcertHalls.value = true;
  try {
    const response = await ApiService.get(`/concerthalls/by-country/${selectedCountry.value}/`);
    concertHalls.value = response.data;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load concert halls', life: 3000 });
  } finally {
    loadingConcertHalls.value = false;
  }
};

watch(selectedCountry, () => {
  selectedConcertHall.value = null;
  concertHalls.value = [];
  if (selectedCountry.value) {
    loadConcertHalls();
  }
});

const generateEvent = async () => {
    const payload = {
    country_code: selectedCountry.value,
    concert_hall_id: selectedConcertHall.value,
    genre_family_name: selectedGenreFamily.value,
    event_start: format(eventStart.value, "yyyy-MM-dd'T'HH:mm:ss"),
    taille_casting: castingSize.value,
    quality_score: qualityScore.value,
    custom_title: customTitle.value
    };
    const response = await ApiService.post('/generate-event/', payload);
    console.log(response)
    generatedEvent.value = response.data;
    showValidationDialog.value = true;
};

const validateEvent = async () => {
    const payload = {
      title: generatedEvent.value.event_preview.title,
      event_start: generatedEvent.value.event_preview.event_start,
      event_end: generatedEvent.value.event_preview.event_end,
      concert_hall_id: generatedEvent.value.event_preview.concert_hall,
      country: generatedEvent.value.event_preview.country,
      artist_ids: generatedEvent.value.casting.map(artist => artist.id)
    };
    await ApiService.post('/validate-event/', payload);
    toast.add({ severity: 'success', summary: 'Success', detail: 'Event validated!', life: 3000 });
    showValidationDialog.value = false;
};

onMounted(async () => {
  await loadCountries();
  await loadGenreFamilies();
});
</script>

<template>
  <div class="card">
    <h2 class="text-2xl font-bold mb-6">Generate New Event</h2>

    <div class="flex flex-col gap-6">

      <div class="flex gap-4 items-center">
        <label class="font-semibold w-32">Country</label>
        <Dropdown
          v-model="selectedCountry"
          :options="countries.map(c => ({ label: c.name, value: c.code }))"
          optionLabel="label"
          optionValue="value"
          placeholder="Select a Country"
          class="w-full"
        />
      </div>

      <div class="flex gap-4 items-center">
        <label class="font-semibold w-32">Concert Hall</label>
        <Dropdown
          v-model="selectedConcertHall"
          :options="concertHalls.map(h => ({ label: h.name, value: h.id }))"
          optionLabel="label"
          optionValue="value"
          placeholder="Select a Concert Hall"
          class="w-full"
          :loading="loadingConcertHalls"
          :disabled="!selectedCountry"
        />
      </div>

      <div class="flex gap-4 items-center">
        <label class="font-semibold w-32">Genre Family</label>
        <Dropdown
          v-model="selectedGenreFamily"
          :options="genreFamilies"
          placeholder="Select a Genre Family"
          class="w-full"
        />
      </div>

      <div class="flex gap-4 items-center">
        <label class="font-semibold w-32">Event Start</label>
        <Calendar
        v-model="eventStart"
        showTime
        hourFormat="24"
        dateFormat="yy-mm-dd"
        class="w-full"
        />
      </div>

      <div class="flex gap-4 items-center">
        <label class="font-semibold w-32">Casting Size</label>
        <InputNumber v-model="castingSize" class="w-full" :min="1" :step="1" />
      </div>

      <div class="flex gap-4 items-center">
        <label class="font-semibold w-32">Quality Score (from 0 to 5)</label>
        <InputNumber v-model="qualityScore"  class="w-full" :min="0" :max="5" :step="1" placeholder="0 - 5" />
      </div>

      <div class="flex gap-4 items-center">
        <label class="font-semibold w-32">Custom Title</label>
        <InputText v-model="customTitle" class="w-full" placeholder="Your Custom Title" />
      </div>

      <div class="flex justify-end">
        <Button label="Generate Event" @click="generateEvent" 
          :disabled="!selectedConcertHall || !selectedGenreFamily || !eventStart" />
      </div>

    </div>

    <Dialog v-model:visible="showValidationDialog" modal header="Validate Generated Event" :style="{ width: '40rem' }">
        <div v-if="generatedEvent">
            <div class="mb-6">
                <h3 class="text-xl font-bold mb-2">Event Preview</h3>
                <p><b>Title:</b> {{ generatedEvent.event_preview?.title }}</p>
                <p><b>Event Start:</b> {{ generatedEvent.event_preview?.event_start }}</p>
                <p><b>Event End:</b> {{ generatedEvent.event_preview?.event_end }}</p>
                <p><b>Country:</b> {{ generatedEvent.event_preview?.country }}</p>
                <p><b>Concert Hall ID:</b> {{ generatedEvent.event_preview?.concert_hall }}</p>
            </div>

            <div class="mb-6">
                <h3 class="text-xl font-bold mb-2">Casting</h3>
                <ul class="list-disc list-inside">
                <li v-for="artist in generatedEvent.casting || []" :key="artist.id">
                    <b>{{ artist.artistName }}</b> ({{ artist.famille_musicale }}) - Popularity: {{ artist.popularity }} - Score: {{ artist.score }}
                </li>
                </ul>
            </div>

            <div class="flex justify-end gap-2">
                <Button label="Cancel" severity="secondary" outlined @click="showValidationDialog = false" />
                <Button label="Validate" @click="validateEvent" />
            </div>
        </div>

    </Dialog>

  </div>
</template>