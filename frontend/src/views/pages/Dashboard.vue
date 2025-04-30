<script setup>
import {
  VMap,
  VMapOsmTileLayer,
  VMapZoomControl
} from 'vue-map-ui';
import { ref, onMounted } from 'vue';
import { ApiService } from '@/services/api';
import { useToast } from 'primevue/usetoast';
import L from 'leaflet';
import customGeoJson from '@/assets/custom.geo.json';

const toast = useToast();

const mapRef = ref();
const leafletMap = ref(null);        // Real Leaflet map instance
const geoJsonLayer = ref(null);      // Highlighted country layer

const countries = ref([]);
const selectedCountry = ref(null);
const demographics = ref(null);
const loadingCountries = ref(false);

// Called once when map is ready
const onMapReady = (mapInstance) => {
  leafletMap.value = mapInstance;
  console.log('Leaflet map is ready');
};

// Load countries + demographics
const loadCountries = async () => {
  loadingCountries.value = true;
  try {
    const response = await ApiService.get('/countries/');
    countries.value = response.data.map(country => ({
      label: country.name || country.code,
      value: country.code,
      demographics: country.demographics
    }));
  } finally {
    loadingCountries.value = false;
  }
};

// Highlight selected country on map
const highlightCountry = (code) => {
  if (!leafletMap.value || !code) {
    console.warn('Leaflet map not ready yet or code missing.');
    return;
  }

  const selectedCode = code.trim().toUpperCase();

  // Remove existing highlight
  if (geoJsonLayer.value) {
    leafletMap.value.removeLayer(geoJsonLayer.value);
    geoJsonLayer.value = null;
  }

  // Match GeoJSON feature
  const getFeatureCode = (f) => {
    const code = f.properties.iso_a2_eh || f.properties.iso_a2 || f.properties.postal;
    return code?.trim().toUpperCase();
  };

  const feature = customGeoJson.features.find(f => {
    const codeMatch = getFeatureCode(f) === selectedCode;
    const isCountry = f.properties.type !== 'Dependency' && f.properties.type !== 'Lease';
    return codeMatch && isCountry;
  });

  if (!feature) {
    console.warn(`No GeoJSON match for code: ${selectedCode}`);
    return;
  }

  // Add highlight and zoom to bounds
  geoJsonLayer.value = L.geoJSON(feature, {
    style: {
      color: 'green',
      weight: 2,
      fillOpacity: 0.4
    }
  }).addTo(leafletMap.value);

  leafletMap.value.fitBounds(geoJsonLayer.value.getBounds());
};

// When a country is selected
const onCountryChange = (e) => {
  const country = countries.value.find(c => c.value === e.value);
  if (country) {
    selectedCountry.value = country.value;
    demographics.value = country.demographics;


  }
};

onMounted(loadCountries);
</script>

<template>
  <VMap ref="mapRef" style="height: 400px;" @ready="onMapReady">
    <VMapOsmTileLayer />
    <VMapZoomControl />
  </VMap>

  <div class="card mt-4">
    <h2 class="text-2xl font-bold mb-6">Demographics by Country</h2>

    <div class="mb-6">
      <label class="block mb-2 font-semibold">Select a Country:</label>
      <Dropdown
        v-model="selectedCountry"
        :options="countries"
        optionLabel="label"
        optionValue="value"
        placeholder="Select a country"
        class="w-full md:w-30rem"
        @change="onCountryChange"
        :loading="loadingCountries"
      />
    </div>

    <div v-if="demographics" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div><strong>Country:</strong> {{ demographics.country }}</div>
      <div><strong>Average Online Ticket Purchase Rate:</strong> {{ demographics.average_online_ticket_purchase_rate ?? 'N/A' }}</div>
      <div><strong>Average Concert Participation Rate:</strong> {{ demographics.average_concert_participation_rate ?? 'N/A' }}</div>
      <div><strong>Quintile Avg Cultural Spending Per Capita:</strong> {{ demographics.quintile_average_cultural_spending_per_capita ?? 'N/A' }}</div>
      <div><strong>Annual Avg Cultural Spending Per Capita:</strong> {{ demographics.annual_average_cultural_spending_per_capita ?? 'N/A' }}</div>
      <div><strong>Mean Estimated Cultural Expenses Until 2030:</strong> {{ demographics.mean_estimated_cultural_expenses_until_2030 ?? 'N/A' }}</div>
      <div><strong>Spotify Streams Total:</strong> {{ demographics.spotify_streams_total_per_country ?? 'N/A' }}</div>
      <div><strong>Number of Tracks:</strong> {{ demographics.number_of_tracks_per_country ?? 'N/A' }}</div>
      <div><strong>Top Chart Presence:</strong> {{ demographics.top_chart_presence_per_country ?? 'N/A' }}</div>
      <div><strong>Average Concert Audience:</strong> {{ demographics.average_concert_audience_per_country ?? 'N/A' }}</div>
      <div><strong>Average Cultural Spending Per Capita:</strong> {{ demographics.average_cultural_spending_per_capita ?? 'N/A' }}</div>
      <div><strong>Country Cluster:</strong> {{ demographics.country_cluster ?? 'N/A' }}</div>
    </div>

    <div v-else class="text-center text-gray-500">
      Please select a country to view demographics.
    </div>
  </div>
</template>
y