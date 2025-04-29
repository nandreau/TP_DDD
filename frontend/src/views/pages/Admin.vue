<script setup>
import { ref, onMounted } from 'vue';
import { FilterMatchMode } from '@primevue/core/api';
import { useConfirm } from 'primevue/useconfirm';
import { useToast } from 'primevue/usetoast';
import { ApiService } from '@/services/api';

const confirm = useConfirm();
const toast = useToast();

const users = ref([]);
const selectedUsers = ref([]);
const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const visibleUpdate = ref(false);
const visibleAdd = ref(false); // <-- ADD THIS
const formUser = ref({
    username: '',
    email: '',
    password: '',
    role: ''
});
const selectedUserId = ref(null);

// For Add Dialog Roles
const roles = ref([
    { name: 'Admin', value: 'admin' },
    { name: 'Artist', value: 'artist' },
    { name: 'Organizer', value: 'organizer' }
]);

const selectedRole = ref(roles.value[0]); // <-- For role selection in Add

const loadUsers = async () => {
    try {
        const response = await ApiService.get('/admin/users');
        users.value = response.data;
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load users', life: 3000 });
    }
};
onMounted(loadUsers);

const openAddDialog = () => {
    formUser.value = { username: '', email: '', password: '', role: '' };
    selectedRole.value = roles.value[0];
    visibleAdd.value = true;
};

const saveNewUser = async () => {
    if (!formUser.value.username || !formUser.value.email || !formUser.value.password || !selectedRole.value) {
        toast.add({
            severity: 'warn',
            summary: 'Validation Error',
            detail: 'Please fill in all fields before saving.',
            life: 3000
        });
        return;
    }
    console.log(formUser.value.username, formUser.value.email, formUser.value.password, selectedRole.value.value)
    await ApiService.post('/admin/users/', {
        username: formUser.value.username,
        email: formUser.value.email,
        password: formUser.value.password,
        role: selectedRole.value.value
    });

    toast.add({ severity: 'success', summary: 'Success', detail: 'User created', life: 3000 });
    visibleAdd.value = false;
    await loadUsers();
};

const openUpdateDialog = () => {
    if (selectedUsers.value.length === 1) {
        const selected = selectedUsers.value[0];
        selectedUserId.value = selected.id;

        formUser.value = {
            username: selected.username,
            email: selected.email,
            password: '',
            role: selected.role
        };
        visibleUpdate.value = true;
    }
};

const saveUserUpdate = async () => {
    const { username, email, password, role } = formUser.value;
    if (!username || !email || !password || !role) {
        toast.add({
            severity: 'warn',
            summary: 'Validation Error',
            detail: 'Please fill in all fields before saving.',
            life: 3000
        });
        return;
    }

    await ApiService.patch(`/admin/users/${selectedUserId.value}/`, { ...formUser.value });
    toast.add({ severity: 'success', summary: 'Success', detail: 'User updated', life: 3000 });
    visibleUpdate.value = false;
    await loadUsers();
    selectedUsers.value = [];
};

const deleteUsers = () => {
    confirm.require({
        message: selectedUsers.value.length > 1
            ? 'Do you want to delete these users?'
            : 'Do you want to delete this user?',
        header: 'Confirmation',
        rejectLabel: 'Cancel',
        acceptLabel: 'Delete',
        rejectProps: { severity: 'secondary', outlined: true },
        acceptProps: { severity: 'danger' },
        accept: async () => {
            const promises = selectedUsers.value.map(user =>
                ApiService.delete(`/admin/users/${user.id}/`)
            );
            await Promise.all(promises);
            toast.add({ severity: 'success', summary: 'Deleted', detail: 'User(s) deleted', life: 3000 });
            await loadUsers();
            selectedUsers.value = [];
        }
    });
};
</script>

<template>
    <div class="card">
        <DataTable
            v-model:filters="filters"
            showGridlines
            :globalFilterFields="['username', 'email', 'role']"
            v-model:selection="selectedUsers"
            paginator
            :rows="10"
            :rowsPerPageOptions="[5, 10, 20]"
            :value="users"
            removableSort
            tableStyle="min-width: 50rem"
        >
            <template #header>
                <div class="flex justify-between items-center">
                    <div class="flex gap-2">
                        <Button
                            @click="openAddDialog"
                            label="Add"
                            severity="sucess"
                        />
                        <Button
                            @click="openUpdateDialog"
                            label="Update"
                            severity="warn"
                            :disabled="!selectedUsers || selectedUsers.length !== 1"
                        />
                        <Button
                            @click="deleteUsers"
                            label="Delete"
                            severity="danger"
                            :disabled="!selectedUsers || selectedUsers.length < 1"
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

            <Column selectionMode="multiple" headerStyle="width: 3rem" />
            <Column field="username" header="Username" sortable />
            <Column field="email" header="Email" sortable />
            <Column field="first_name" header="First Name" sortable />
            <Column field="last_name" header="Last Name" sortable />
            <Column field="role" header="Role" sortable />
        </DataTable>
    </div>
    <Dialog v-model:visible="visibleUpdate" modal header="Confirmation" :style="{ width: '25rem' }">
        <span class="text-surface-500 dark:text-surface-400 block mb-8">Update User informations.</span>

        <div class="flex items-center gap-4 mb-4">
            <label for="username" class="font-semibold w-24">Username</label>
            <InputText id="username" class="flex-auto" v-model="formUser.username" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4 mb-4">
            <label for="email" class="font-semibold w-24">Email</label>
            <InputText id="email" class="flex-auto" v-model="formUser.email" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4 mb-4">
            <label for="password" class="font-semibold w-24">Password</label>
            <InputText id="password" class="flex-auto" v-model="formUser.password" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4 mb-8">
            <label for="role" class="font-semibold w-24">Role</label>
            <InputText id="role" class="flex-auto" v-model="formUser.role" autocomplete="off" />
        </div>

        <div class="flex justify-end gap-2">
            <Button type="button" label="Cancel" severity="secondary" @click="visibleUpdate = false" outlined/>
            <Button type="button" label="Save" @click="saveUserUpdate" />
        </div>
    </Dialog>
    <Dialog v-model:visible="visibleAdd" modal header="Add New User" :style="{ width: '25rem' }">
        <span class="text-surface-500 dark:text-surface-400 block mb-8">Fill the new user's information.</span>

        <div class="flex items-center gap-4 mb-4">
            <label for="username" class="font-semibold w-24">Username</label>
            <InputText id="username" class="flex-auto" v-model="formUser.username" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4 mb-4">
            <label for="email" class="font-semibold w-24">Email</label>
            <InputText id="email" class="flex-auto" v-model="formUser.email" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4 mb-4">
            <label for="password" class="font-semibold w-24">Password</label>
            <InputText id="password" class="flex-auto" v-model="formUser.password" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4 mb-8">
            <label for="role" class="font-semibold w-24">Role</label>
            <Dropdown v-model="selectedRole" :options="roles" optionLabel="name" class="flex-auto" />
        </div>

        <div class="flex justify-end gap-2">
            <Button type="button" label="Cancel" severity="secondary" @click="visibleAdd = false" outlined/>
            <Button type="button" label="Save" @click="saveNewUser" />
        </div>
    </Dialog>
</template>