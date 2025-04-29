<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ApiService } from '@/services/api'
import { getToast } from '@/composables/usePrimeToast'

const username = ref('')
const password = ref('')
const router = useRouter()
const toast = getToast()
const loading = ref(false)
const checked = ref(false)

const handleLogin = async () => {
  loading.value = true
  try {
    const response = await ApiService.post('/login/', {
      username: username.value,
      password: password.value
    })

    const token = response.data.token
    localStorage.setItem('authToken', token)
    const user = response.data.user

    toast.add({
      severity: 'success',
      summary: 'Login Successful',
      detail: 'Welcome back ' + user.username + '!',
      life: 3000
    });

    router.push('/');
  } finally {
    loading.value = false;
  }
};
</script>

<template>
    <div class="bg-surface-50 dark:bg-surface-950 flex items-center justify-center min-h-screen min-w-[100vw] overflow-hidden">
        <div class="flex flex-col items-center justify-center">
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 80%)">
                <div class="w-full bg-surface-0 dark:bg-surface-900 py-20 px-8 sm:px-20" style="border-radius: 53px">
                    <div class="text-center mb-8">
                        <svg class="mb-8 w-16 shrink-0 mx-auto" fill="var(--primary-color)" viewBox="0 0 20 20"><path d="M15.75 8l-3.74-3.75a3.99 3.99 0 0 1 6.82-3.08A4 4 0 0 1 15.75 8zm-13.9 7.3l9.2-9.19 2.83 2.83-9.2 9.2-2.82-2.84zm-1.4 2.83l2.11-2.12 1.42 1.42-2.12 2.12-1.42-1.42zM10 15l2-2v7h-2v-5z"/></svg>
                        <div class="text-surface-900 dark:text-surface-0 text-3xl font-medium mb-4">Welcome to Concert App!</div>
                        <span class="text-muted-color font-medium">Sign in to continue</span>
                    </div>

                    <div>
                        <label for="username1" class="block text-surface-900 dark:text-surface-0 text-xl font-medium mb-2">Username</label>
                        <InputText id="username1" type="text" placeholder="Username" class="w-full md:w-[30rem] mb-8" v-model="username" />

                        <label for="password1" class="block text-surface-900 dark:text-surface-0 font-medium text-xl mb-2">Password</label>
                        <Password id="password1" v-model="password" placeholder="Password" :toggleMask="true" class="mb-4" fluid :feedback="false"></Password>

                        <div class="flex items-center justify-between mt-2 mb-8 gap-8">
                            <div class="flex items-center">
                                <Checkbox v-model="checked" id="rememberme1" binary class="mr-2"></Checkbox>
                                <label for="rememberme1">Remember me</label>
                            </div>
                            <router-link to="/auth/register/" class="font-medium no-underline ml-2 text-right cursor-pointer text-primary">No account?</router-link>
                        </div>
                        <Button label="Sign In" class="w-full" :disabled="loading" @click="handleLogin"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
