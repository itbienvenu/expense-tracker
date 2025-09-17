<template>
  <div class="card bg-dark text-white border-secondary mb-4">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h4 class="mb-0">Transactions</h4>
      <button @click="showAddForm = true" class="btn btn-warning">+ Add New Transaction</button>
    </div>

    <div v-if="showAddForm || editingTransaction" class="card-body">
      <form @submit.prevent="saveTransaction">
        <div class="mb-3">
          <label for="title" class="form-label">Title</label>
          <input id="title" v-model="title" class="form-control bg-dark text-light border-secondary" placeholder="Title" required />
        </div>
        <div class="mb-3">
          <label for="type" class="form-label">Type</label>
          <select id="type" v-model="type" class="form-select bg-dark text-light border-secondary" required>
            <option value="expense">Expense</option>
            <option value="income">Income</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="amount" class="form-label">Amount</label>
          <input id="amount" v-model="amount" type="number" step="0.01" class="form-control bg-dark text-light border-secondary" placeholder="Amount" required />
        </div>
        <div class="mb-3">
          <label for="date" class="form-label">Date</label>
          <input id="date" v-model="date" type="date" class="form-control bg-dark text-light border-secondary" required />
        </div>
        <div class="mb-3">
          <label for="category" class="form-label">Category</label>
          <select id="category" v-model="selectedCategory" class="form-select bg-dark text-light border-secondary" required>
            <option disabled value="">Please select a category</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>
        
        <div class="d-flex gap-2">
          <button type="submit" class="btn btn-warning">{{ editingTransaction ? 'Update' : 'Create' }}</button>
          <button @click="cancelEdit" type="button" class="btn btn-outline-light">Cancel</button>
        </div>
      </form>
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

    <ul class="list-group list-group-flush">
      <li v-for="transaction in transactions" :key="transaction.id" class="list-group-item d-flex justify-content-between align-items-center bg-dark text-white border-secondary">
        <div>
          <h6 class="mb-1">{{ transaction.title }}</h6>
          <small class="text-muted">{{ new Date(transaction.date).toLocaleDateString() }}</small>
          <div>
            <span v-for="cat in transaction.categories" :key="cat.id" class="badge rounded-pill bg-secondary me-1">{{ cat.name }}</span>
          </div>
        </div>
        <div class="d-flex align-items-center gap-2">
          <span class="fw-bold fs-5" :class="{'text-danger': transaction.amount < 0, 'text-success': transaction.amount >= 0}">
            ${{ Math.abs(transaction.amount).toFixed(2) }}
          </span>
          <div class="btn-group">
            <button @click="editTransaction(transaction)" class="btn btn-sm btn-outline-info">Edit</button>
            <button @click="deleteTransaction(transaction.id)" class="btn btn-sm btn-outline-danger">Delete</button>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
const BASE_API_URL = import.meta.env.VITE_APP_API_URL;

const transactions = ref([]);
const categories = ref([]);
const showAddForm = ref(false);
const editingTransaction = ref(null);
const title = ref('');
const amount = ref(0);
const date = ref('');
const selectedCategory = ref('');
const type = ref('expense');

const filterOptions = ref({
  startDate: '',
  endDate: '',
  category_ids: [],
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
    
    // We'll keep the sort and order fixed to 'date' and 'desc' for simplicity
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
    category_ids: [],
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
      editingTransaction.value = null;
    } else {
      await axios.post(`${BASE_API_URL}/tracker/transactions`, payload, { headers: getHeaders() });
      showAddForm.value = false;
    }
    resetForm();
    fetchFilteredTransactions();
  } catch (error) {
    console.error('Failed to save transaction:', error);
  }
};

const editTransaction = (transaction) => {
  editingTransaction.value = transaction;
  title.value = transaction.title;
  date.value = new Date(transaction.date).toISOString().split('T')[0];
  selectedCategory.value = transaction.categories[0]?.id || '';
  amount.value = Math.abs(transaction.amount);
  type.value = transaction.amount < 0 ? 'expense' : 'income';
  showAddForm.value = true;
};

const cancelEdit = () => {
  editingTransaction.value = null;
  showAddForm.value = false;
  resetForm();
};

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
});
</script>