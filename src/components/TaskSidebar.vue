<template>
  <aside class="sidebar">
    <ul>
      <li @click="$emit('filter', 'all')">Всі</li>
      <li @click="$emit('filter', 'important')">Важливі</li>
      <li @click="$emit('filter', 'completed')">Виконані</li>
    </ul>
  </aside>
</template>

<script>
export default {
  props: {
    currentFilter: {
      type: String,
      default: 'all',
    }
  },
  data() {
    return {
      filters: [
        { key: 'all', label: 'Всі' },
        { key: 'important', label: 'Важливі' },
        { key: 'completed', label: 'Виконані' }
      ]
    };
  },
  methods: {
    applyFilter(filter) {
      this.$emit('filter', filter);
    }
  }
};
</script>

<style>
.sidebar {
  width: 250px;
  background-color: #f8f9fa;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  position: fixed;
  height: 100%;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin: 15px 0;
  cursor: pointer;
  font-size: 18px;
  color: #007bff;
}

.sidebar li:hover {
  text-decoration: underline;
}
</style>
