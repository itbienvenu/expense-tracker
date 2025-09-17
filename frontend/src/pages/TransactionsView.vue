<template>
<div>  
  <div class="card bg-dark text-white border-secondary mb-4">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h4 class="mb-0">Transactions</h4>
      <button @click="openAddModal" class="btn btn-warning">+ Add New Transaction</button>
    </div>

    <div class="card bg-dark text-white border-secondary mb-4">
      <div class="card-body">
        <h5 class="card-title">Filter & Sort Transactions</h5>
        <form @submit.prevent="fetchFilteredTransactions">
          <div class="row g-3">
            <div class="col-md-4">
              <label for="startDate" class="form-label">Start Date</label>
              <input type="date" class="form-control bg-dark text-light border-secondary" id="startDate" v-model="filterOptions.startDate">
            </div>
            <div class="col-md-4">
              <label for="endDate" class="form-label">End Date</label>
              <input type="date" class="form-control bg-dark text-light border-secondary" id="endDate" v-model="filterOptions.endDate">
            </div>
            <div class="col-md-4">
              <label for="categoryFilter" class="form-label">Category</label>
              <select class="form-select bg-dark text-light border-secondary" id="categoryFilter" v-model="filterOptions.category_ids">
                <option value="">All Categories</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
              </select>
            </div>
            <div class="col-12 d-flex justify-content-end gap-2">
              <button type="submit" class="btn btn-warning">Apply Filters</button>
              <button type="button" class="btn btn-outline-light" @click="resetFilters">Reset</button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <div class="card-body">
        <div v-if="transactions.length === 0" class="text-center text-muted py-4">
            No transactions found for the selected filters.
        </div>
        <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            <div class="col" v-for="transaction in transactions" :key="transaction.id">
                <div class="transaction-card card h-100 bg-dark text-white border-secondary shadow-sm">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title text-truncate mb-1">{{ transaction.title }}</h5>
                        <h6 class="card-subtitle mb-2 text-muted small">{{ new Date(transaction.date).toLocaleDateString() }}</h6>
                        
                        <div class="d-flex flex-wrap gap-1 mb-3">
                            <span v-for="cat in transaction.categories" :key="cat.id" class="badge rounded-pill bg-secondary">{{ cat.name }}</span>
                        </div>

                        <div class="mt-auto d-flex justify-content-between align-items-center">
                            <span class="fw-bold fs-4" :class="{'text-danger': transaction.amount < 0, 'text-success': transaction.amount >= 0}">
                                ${{ Math.abs(transaction.amount).toFixed(2) }}
                            </span>
                            <div class="btn-group">
                                <button @click="openEditModal(transaction)" class="btn btn-sm btn-outline-info">Edit</button>
                                <button @click="deleteTransaction(transaction.id)" class="btn btn-sm btn-outline-danger">Delete</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>

  <div class="modal fade" id="transactionModal" tabindex="-1" aria-labelledby="transactionModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-dark text-white border-secondary">
        <div class="modal-header border-secondary">
          <h5 class="modal-title" id="transactionModalLabel">{{ editingTransaction ? 'Edit Transaction' : 'Add New Transaction' }}</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form @submit.prevent="saveTransaction">
          <div class="modal-body">
            <div class="mb-3">
              <label for="modalTitle" class="form-label">Title</label>
              <input id="modalTitle" v-model="title" class="form-control bg-dark text-light border-secondary" placeholder="Title" required />
            </div>
            <div class="mb-3">
              <label for="modalType" class="form-label">Type</label>
              <select id="modalType" v-model="type" class="form-select bg-dark text-light border-secondary" required>
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="modalAmount" class="form-label">Amount</label>
              <input id="modalAmount" v-model="amount" type="number" step="0.01" class="form-control bg-dark text-light border-secondary" placeholder="Amount" required />
            </div>
            <div class="mb-3">
              <label for="modalDate" class="form-label">Date</label>
              <input id="modalDate" v-model="date" type="date" class="form-control bg-dark text-light border-secondary" required />
            </div>
            <div class="mb-3">
              <label for="modalCategory" class="form-label">Category</label>
              <select id="modalCategory" v-model="selectedCategory" class="form-select bg-dark text-light border-secondary" required>
                <option disabled value="">Please select a category</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
              </select>
            </div>
          </div>
          <div class="modal-footer border-secondary">
            <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">Cancel</button>
            <button type="submit" class="btn btn-warning">{{ editingTransaction ? 'Update' : 'Create' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>  
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { Modal } from 'bootstrap'; // Import Bootstrap's Modal JavaScript class

// Access the global API URL
const BASE_API_URL = import.meta.env.VITE_APP_API_URL; 

const transactions = ref([]);
const categories = ref([]);
// showAddForm is no longer needed as a direct toggle for form visibility
const editingTransaction = ref(null);
const title = ref('');
const amount = ref(0);
const date = ref('');
const selectedCategory = ref('');
const type = ref('expense');

let transactionModalInstance = null; // To hold the Bootstrap modal instance

const filterOptions = ref({
  startDate: '',
  endDate: '',
  category_ids: '', // Reset to empty string for single select
  minAmount: null,
  maxAmount: null,
  sort_by: 'date',
  order: 'desc',
});

const getHeaders = () => {
  const token = localStorage.getItem('accessToken');
  return { Authorization: `Bearer ${token}` };
};

const fetchFilteredTransactions = async () => {
  try {
    const params = {};
    if (filterOptions.value.startDate) params.start_date = filterOptions.value.startDate;
    if (filterOptions.value.endDate) params.end_date = filterOptions.value.endDate;
    if (filterOptions.value.category_ids && filterOptions.value.category_ids.length > 0) {
      params.category_ids = Array.isArray(filterOptions.value.category_ids) ? filterOptions.value.category_ids.join(',') : filterOptions.value.category_ids;
    }
    
    params.sort_by = 'date';
    params.order = 'desc';
    
    const response = await axios.get(`${BASE_API_URL}/reports/`, { 
      headers: getHeaders(),
      params: params
    });
    transactions.value = response.data;
  } catch (error) {
    console.error('Failed to fetch filtered transactions:', error);
  }
};

const resetFilters = () => {
  filterOptions.value = {
    startDate: '',
    endDate: '',
    category_ids: '',
    minAmount: null,
    maxAmount: null,
    sort_by: 'date',
    order: 'desc',
  };
  fetchFilteredTransactions();
};

const fetchCategories = async () => {
  try {
    const response = await axios.get(`${BASE_API_URL}/tracker/categories`, { headers: getHeaders() });
    categories.value = response.data;
  } catch (error) {
    console.error('Failed to fetch categories:', error);
  }
};

const openAddModal = () => {
  editingTransaction.value = null; // Clear editing state
  resetForm(); // Clear form fields
  transactionModalInstance.show(); // Show the modal
};

const openEditModal = (transaction) => {
  editingTransaction.value = transaction;
  title.value = transaction.title;
  date.value = new Date(transaction.date).toISOString().split('T')[0];
  selectedCategory.value = transaction.categories[0]?.id || '';
  amount.value = Math.abs(transaction.amount);
  type.value = transaction.amount < 0 ? 'expense' : 'income';
  transactionModalInstance.show(); // Show the modal
};

const saveTransaction = async () => {
  const finalAmount = type.value === 'expense' ? -Math.abs(amount.value) : Math.abs(amount.value);
  const payload = {
    title: title.value,
    amount: parseFloat(finalAmount),
    date: new Date(date.value).toISOString(),
    category_ids: [selectedCategory.value],
  };

  try {
    if (editingTransaction.value) {
      await axios.patch(`${BASE_API_URL}/tracker/transactions/${editingTransaction.value.id}`, payload, { headers: getHeaders() });
    } else {
      await axios.post(`${BASE_API_URL}/tracker/transactions`, payload, { headers: getHeaders() });
    }
    
    transactionModalInstance.hide(); // Hide the modal on success
    resetForm(); // Clear form fields
    fetchFilteredTransactions(); // Refresh the list
  } catch (error) {
    console.error('Failed to save transaction:', error);
  }
};

// cancelEdit is now handled by closing the modal
const resetForm = () => {
  title.value = '';
  amount.value = 0;
  date.value = '';
  selectedCategory.value = '';
  type.value = 'expense';
};

const deleteTransaction = async (id) => {
  if (confirm('Are you sure you want to delete this transaction?')) {
    try {
      await axios.delete(`${BASE_API_URL}/tracker/transactions/${id}`, { headers: getHeaders() });
      fetchFilteredTransactions();
    } catch (error) {
      console.error('Failed to delete transaction:', error);
    }
  }
};

onMounted(() => {
  fetchCategories();
  fetchFilteredTransactions();
  // Initialize the Bootstrap modal instance
  const modalElement = document.getElementById('transactionModal');
  if (modalElement) {
    transactionModalInstance = new Modal(modalElement);
    // Optional: Add event listener to clear form when modal closes
    modalElement.addEventListener('hidden.bs.modal', () => {
      if (!editingTransaction.value) { // Only reset if not editing (i.e., new transaction)
        resetForm();
      }
      editingTransaction.value = null; // Always clear editing state on close
    });
  }
});
</script>

<style scoped>
.transaction-card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}
.transaction-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.card-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>