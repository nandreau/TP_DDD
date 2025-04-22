<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ApiService } from '@/services/api'
import { getToast } from '@/composables/usePrimeToast'

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const router = useRouter()
const toast = getToast()

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    toast.add({
      severity: 'error',
      summary: 'Passwords do not match',
      detail: 'Please make sure both passwords are the same.',
      life: 3000
    })
    return
  }

  loading.value = true
  try {
    await ApiService.post('/register', {
      username: username.value,
      email: email.value,
      password: password.value
    })

    toast.add({
      severity: 'success',
      summary: 'Registration Successful',
      detail: 'You can now sign in.',
      life: 3000
    })

    router.push('/login')
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Registration Failed',
      detail: error?.response?.data?.message || 'Something went wrong.',
      life: 3000
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="bg-surface-50 dark:bg-surface-950 flex items-center justify-center min-h-screen min-w-[100vw] overflow-hidden">
    <div class="flex flex-col items-center justify-center">
      <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 80%)">
        <div class="w-full bg-surface-0 dark:bg-surface-900 py-20 px-8 sm:px-20" style="border-radius: 53px">
          <div class="text-center mb-8">
            <div class="text-surface-900 dark:text-surface-0 text-3xl font-medium mb-4">Create your account</div>
            <span class="text-muted-color font-medium">Join us today!</span>
          </div>

          <div>
            <label for="email" class="block text-surface-900 dark:text-surface-0 text-xl font-medium mb-2">Email</label>
            <InputText id="email" type="text" placeholder="Email address" class="w-full md:w-[30rem] mb-6" v-model="email" />

            <label for="username" class="block text-surface-900 dark:text-surface-0 text-xl font-medium mb-2">Username</label>
            <InputText id="username" type="text" placeholder="Username" class="w-full md:w-[30rem] mb-6" v-model="username" />

            <label for="password" class="block text-surface-900 dark:text-surface-0 font-medium text-xl mb-2">Password</label>
            <Password id="password" v-model="password" placeholder="Password" :toggleMask="true" class="mb-6" fluid :feedback="false" />

            <label for="confirmPassword" class="block text-surface-900 dark:text-surface-0 font-medium text-xl mb-2">Confirm Password</label>
            <Password id="confirmPassword" v-model="confirmPassword" placeholder="Repeat password" :toggleMask="true" class="mb-8" fluid :feedback="false" />

            <Button label="Register" class="w-full" :disabled="loading" @click="handleRegister" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
