<template>
<div :id="mapId"></div>
</template>

  
<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default {
    name: 'LeafletMap',
    props: {
        geojsonData: Object,
    },
    data() {
        return {
            mapId: 'leaflet-map',
            mapInstance: null,
            layerControlInstance: null,
            geoJsonLayer: null,
        };
    },
    mounted() {
        this.initMap();
        this.$emit('ready', this.mapInstance);
    },
    methods: {
        initMap() {
            const leafletMap = L.map(this.mapId, {});

            const tile = L.tileLayer(
                'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '',
                }
            ).addTo(leafletMap);

            this.layerControlInstance = L.control
                .layers({
                    OpenStreetMap: tile,
                })
                .addTo(leafletMap);

            this.mapInstance = leafletMap;
        },
    },
};
</script>

  
<style scoped>
#leaflet-map {
    width: 100%;
    overflow: hidden;
}
</style>
