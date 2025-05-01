<script setup>
import { ref, onMounted, watch } from 'vue';
import { ApiService } from '@/services/api';
import { useToast } from 'primevue/usetoast';
import customGeoJson from '@/assets/custom.geo.json';
import LeafletMap from '@/components/LeafletMap.vue';
import L from 'leaflet';

const toast = useToast();

const leafletMap = ref(null);
const geoJsonLayer = ref(null);
const legendControl = ref(null);
const selectedOverlay = ref(null); // hatch layer

const countries = ref([]);
const selectedCountry = ref(null);
const selectedDemographic = ref(null);
const demographics = ref(null);
const loadingCountries = ref(false);

const availableDemographics = [
  { label: 'Average Online Ticket Purchase Rate', value: 'average_online_ticket_purchase_rate' },
  { label: 'Average Concert Participation Rate', value: 'average_concert_participation_rate' },
  { label: 'Quintile Avg Cultural Spending Per Capital', value: 'quintile_average_cultural_spending_per_capita' },
  { label: 'Annual Avg Cultural Spending Per Capital', value: 'annual_average_cultural_spending_per_capita' },
  { label: 'Mean Estimated Cultural Expenses Until 2030', value: 'mean_estimated_cultural_expenses_until_2030' },
  { label: 'Spotify Streams Total', value: 'spotify_streams_total_per_country' },
  { label: 'Number of Tracks', value: 'number_of_tracks_per_country' },
  { label: 'Top Chart Presence', value: 'top_chart_presence_per_country' },
  { label: 'Average Concert Audience', value: 'average_concert_audience_per_country' },
  { label: 'Average Cultural Spending Per Capital', value: 'average_cultural_spending_per_capita' },
];


const getFeatureCode = (f) => f.properties.iso_a2_eh || f.properties.iso_a2 || f.properties.postal;

const onMapReady = (mapInstance) => {
  leafletMap.value = mapInstance;
  renderBaseLayer(); // show basic map
};

const loadCountries = async () => {
  loadingCountries.value = true;
  try {
    const response = await ApiService.get('/countries/');
    countries.value = response.data.map((country) => ({
      label: country.name || country.code,
      value: country.code,
      demographics: country.demographics,
    }));
  } finally {
    loadingCountries.value = false;
  }
};

const ensureHatchPattern = () => {
  if (document.getElementById('diagonalHatch')) return;

  const svgNS = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(svgNS, 'svg');
  svg.setAttribute('height', 0);
  svg.setAttribute('width', 0);
  svg.style.position = 'absolute';

  const defs = document.createElementNS(svgNS, 'defs');
  const pattern = document.createElementNS(svgNS, 'pattern');
  pattern.setAttribute('id', 'diagonalHatch');
  pattern.setAttribute('patternUnits', 'userSpaceOnUse');
  pattern.setAttribute('width', '8');
  pattern.setAttribute('height', '8');
  pattern.setAttribute('patternTransform', 'rotate(45)');

  const rect = document.createElementNS(svgNS, 'rect');
  rect.setAttribute('width', '4');
  rect.setAttribute('height', '8');
  rect.setAttribute('transform', 'translate(0,0)');
  rect.setAttribute('fill', 'black');

  pattern.appendChild(rect);
  defs.appendChild(pattern);
  svg.appendChild(defs);
  svg.setAttribute('id', 'diagonalHatch');
  document.body.appendChild(svg);
};


const updateSelectCountry = (code) => {
  if (!leafletMap.value) return;

  if (selectedOverlay.value) {
    leafletMap.value.removeLayer(selectedOverlay.value);
    selectedOverlay.value = null;
  }

  const feature = customGeoJson.features.find(f => {
    const featureCode = getFeatureCode(f)?.trim().toUpperCase();
    return featureCode === code;
  });

  if (!feature) return;

  selectedOverlay.value = L.geoJSON(feature, {
    style: {
      color: '#000',
      weight: 2.5,
      fillOpacity: 0
    }
  }).addTo(leafletMap.value);
};

const handleFeatureClick = (feature, layer) => {
  const code = getFeatureCode(feature)?.trim().toUpperCase();
  layer.on('click', () => {
    const match = countries.value.find(c => c.value === code);
    if (!match) return;

    selectedCountry.value = match.value;
    demographics.value = match.demographics;
    updateSelectCountry(match.value);

    if (selectedDemographic.value) {
      const featureMatch = customGeoJson.features.find(f => {
        const featureCode = getFeatureCode(f)?.trim().toUpperCase();
        return featureCode === match.value;
      });

      if (featureMatch && leafletMap.value) {
        const bounds = L.geoJSON(featureMatch).getBounds();
        leafletMap.value.fitBounds(bounds, { maxZoom: 6 });
      }
    }
  });
};

const renderBaseLayer = () => {
  if (!leafletMap.value) return;

  if (geoJsonLayer.value) {
    leafletMap.value.removeLayer(geoJsonLayer.value);
    geoJsonLayer.value = null;
  }

  geoJsonLayer.value = L.geoJSON(customGeoJson, {
    style: {
      fillColor: '#e0e0e0',
      color: '#666',
      weight: 1,
      fillOpacity: 0.4,
    },
    onEachFeature: handleFeatureClick,
  }).addTo(leafletMap.value);

  leafletMap.value.fitBounds(geoJsonLayer.value.getBounds());
};

const renderChoroplethLayer = (metric) => {
  if (!leafletMap.value || !metric) return;

  if (geoJsonLayer.value) {
    leafletMap.value.removeLayer(geoJsonLayer.value);
    geoJsonLayer.value = null;
  }

  const values = countries.value
    .map(c => c.demographics?.[metric])
    .filter(v => typeof v === 'number');

  const min = Math.min(...values);
  const max = Math.max(...values);

  const getColor = (value) => {
    if (value === null || value === undefined || isNaN(value)) return '#ccc';
    const t = (value - min) / (max - min);
    if (t <= 0.0) return '#c5e4bc';
    if (t <= 0.2) return '#3fd318';
    if (t <= 0.4) return '#a6d96a';
    if (t <= 0.6) return '#fdae61';
    if (t <= 0.8) return '#f46d43';
    return '#a50026';
  };

  const createLegendHtml = () => {
    const steps = 5;
    const stepSize = (max - min) / (steps - 1);
    let html = '';
    for (let i = 0; i < steps; i++) {
      const val = min + stepSize * i;
      const color = getColor(val);
      html += `<div style="display:flex;align-items:center;margin-bottom:2px;">
        <div style="background:${color};width:20px;height:12px;margin-right:8px;border:1px solid #ccc;"></div>
        ${val.toFixed(2)}
      </div>`;
    }
    return html;
  };

  geoJsonLayer.value = L.geoJSON(customGeoJson, {
    style: (feature) => {
      const code = getFeatureCode(feature)?.trim().toUpperCase();
      const country = countries.value.find(c => c.value === code);
      const val = country?.demographics?.[metric];
      return {
        fillColor: getColor(val),
        color: '#333',
        weight: 1,
        fillOpacity: 0.6,
      };
    },
    onEachFeature: handleFeatureClick,
  }).addTo(leafletMap.value);

  leafletMap.value.fitBounds(geoJsonLayer.value.getBounds());

  if (legendControl.value) {
    leafletMap.value.removeControl(legendControl.value);
  }

  legendControl.value = L.control({ position: 'bottomright' });
  legendControl.value.onAdd = function () {
    const div = L.DomUtil.create('div', 'info legend');
    div.innerHTML = createLegendHtml();
    div.style.background = '#747474a8';
    div.style.padding = '5px 8px';
    div.style.border = '1px solid #0000004f';
    div.style.borderRadius = '5px';
    div.style.fontSize = '11px';
    div.style.color = 'white';
    return div;
  };
  legendControl.value.addTo(leafletMap.value);
};

const onCountryChange = (e) => {
  const country = countries.value.find((c) => c.value === e.value);
  if (country) {
    selectedCountry.value = country.value;
    demographics.value = country.demographics;
    updateSelectCountry(country.value);

    const feature = customGeoJson.features.find(f => {
      const featureCode = getFeatureCode(f)?.trim().toUpperCase();
      return featureCode === country.value.trim().toUpperCase();
    });

    if (feature && leafletMap.value) {
      const layer = L.geoJSON(feature);
      leafletMap.value.fitBounds(layer.getBounds(), { maxZoom: 6 });
    }
  }
};

watch(selectedDemographic, (val) => {
  if (val) renderChoroplethLayer(val);
  else renderBaseLayer(); // fallback to base if cleared
});

onMounted(loadCountries);
</script>


<template>
  <div class="flex flex-1 gap-5">
    <LeafletMap @ready="onMapReady" />

    <div class="card !p-6 !mb-0">
      <h2 class="text-2xl font-bold mb-4">Demographics</h2>

      <div class="mb-6">
        <div>
          <label class="block mb-2 font-semibold">Select a Country:</label>
          <Dropdown
            v-model="selectedCountry"
            :options="countries"
            optionLabel="label"
            optionValue="value"
            placeholder="Select a country"
            class="w-full"
            @change="onCountryChange"
            :loading="loadingCountries"
            :disabled="!leafletMap"
          />
        </div>

        <div class="mt-3">
          <label class="block mb-2 font-semibold">Select a Demographic:</label>
          <Dropdown
            v-model="selectedDemographic"
            :options="availableDemographics"
            optionLabel="label"
            optionValue="value"
            placeholder="Color countries by..."
            class="w-full"
            :disabled="!leafletMap"
          />
        </div>
      </div>

      <div v-if="demographics" class="grid grid-cols-1 gap-1">
        <div><strong>Country:</strong> {{ demographics.country }}</div>
        <div><strong>Average Online Ticket Purchase Rate:</strong> {{ demographics.average_online_ticket_purchase_rate ?? 'N/A' }}</div>
        <div><strong>Average Concert Participation Rate:</strong> {{ demographics.average_concert_participation_rate ?? 'N/A' }}</div>
        <div><strong>Quintile Avg Cultural Spending Per Capital:</strong> {{ demographics.quintile_average_cultural_spending_per_capita ?? 'N/A' }}</div>
        <div><strong>Annual Avg Cultural Spending Per Capital:</strong> {{ demographics.annual_average_cultural_spending_per_capita ?? 'N/A' }}</div>
        <div><strong>Mean Estimated Cultural Expenses Until 2030:</strong> {{ demographics.mean_estimated_cultural_expenses_until_2030 ?? 'N/A' }}</div>
        <div><strong>Spotify Streams Total:</strong> {{ demographics.spotify_streams_total_per_country ?? 'N/A' }}</div>
        <div><strong>Number of Tracks:</strong> {{ demographics.number_of_tracks_per_country ?? 'N/A' }}</div>
        <div><strong>Top Chart Presence:</strong> {{ demographics.top_chart_presence_per_country ?? 'N/A' }}</div>
        <div><strong>Average Concert Audience:</strong> {{ demographics.average_concert_audience_per_country ?? 'N/A' }}</div>
        <div><strong>Average Cultural Spending Per Capital:</strong> {{ demographics.average_cultural_spending_per_capita ?? 'N/A' }}</div>
        <div><strong>Country Cluster:</strong> {{ demographics.country_cluster ?? 'N/A' }}</div>
      </div>


      <div v-else class="text-center text-gray-500">
        Please select a country to view demographics.
      </div>
    </div>
  </div>
</template>