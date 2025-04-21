import "primeicons/primeicons.css";
import "./style.css";
import "./flags.css";

import { createApp } from "vue";
import PrimeVue from "primevue/config";
import ConfirmationService from 'primevue/confirmationservice'
import DialogService from 'primevue/dialogservice'
import ToastService from 'primevue/toastservice';
import Toast from 'primevue/toast';

import router from './router';
import App from "./App.vue";
import AppState from './plugins/appState.js';
import HeaderComponent from './components/HeaderComponent.vue';
import Emerald from './presets/Emerald.js';

const app = createApp(App);

app.use(PrimeVue, {
    ripple: true,
    theme: {
        preset: Emerald,
        options: {
            prefix: 'p',
            darkModeSelector: '.p-dark',
            cssLayer: false,
        }
    }
});
app.use(AppState);
app.use(ConfirmationService);
app.use(ToastService);
app.use(DialogService);
app.use(router);

app.component('Toast', Toast);
app.component('HeaderComponent', HeaderComponent);

app.mount("#app");
