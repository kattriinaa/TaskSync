<template>
  <div class="side-menu" :class="{ 'dark-mode': isDarkMode }">
    <div class="user-profile" @click="navigateToProfile">
      <img :src="userAvatar" alt="User Avatar" class="avatar" />
      <span class="username">{{ username }}</span>
    </div>
    <div class="filters-btn-wrapper">
      <button class="side-btn filters-btn" @click="toggleFilters">
        Filters
      </button>
      <div v-if="filtersVisible" class="side-filters-popup" :class="{ 'dark-mode': isDarkMode }">
        <select v-model="selectedMonth" @change="applyFilters">
          <option value="">All Months</option>
          <option v-for="month in months" :key="month.value" :value="month.value">
            {{ month.name }}
          </option>
        </select>
        
        <div class="date-input-wrapper">
          <input class="date" type="date" v-model="selectedDate" @change="applyFilters" />
        </div>
        
        <select v-model="selectedDueDate" @change="applyFilters">
          <option value="">All Due Dates</option>
          <option value="today">Today</option>
          <option value="tomorrow">Tomorrow</option>
          <option value="nextWeek">Next Week</option>
        </select>
        
        <button class="clear-filters-btn" @click="clearFilters">
          Clear Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SideMenu',
  props: {
    tasks: {
      type: Array,
      required: true
    },
    currentFilter: {
      type: String,
      default: 'all'
    },
    currentView: {
      type: String,
      default: 'tasks'
    }
  },
  data() {
    return {
      isDarkMode: localStorage.getItem('darkMode') === 'true',
      username: localStorage.getItem('username') || 'User',
      userAvatar: localStorage.getItem('userAvatar') || 'https://via.placeholder.com/50',
      filtersVisible: false,
      selectedMonth: '',
      selectedDate: '',
      selectedDueDate: '',
      months: [
        { name: 'January', value: '01' },
        { name: 'February', value: '02' },
        { name: 'March', value: '03' },
        { name: 'April', value: '04' },
        { name: 'May', value: '05' },
        { name: 'June', value: '06' },
        { name: 'July', value: '07' },
        { name: 'August', value: '08' },
        { name: 'September', value: '09' },
        { name: 'October', value: '10' },
        { name: 'November', value: '11' },
        { name: 'December', value: '12' }
      ]
    }
  },
  methods: {
    navigateToProfile() {
      this.$emit('navigate', 'profile')
    },
    navigateToTasks() {
      this.$emit('navigate', 'tasks')
    },
    navigateToArchive() {
      this.$emit('navigate', 'archive')
    },
    toggleFilters() {
      this.filtersVisible = !this.filtersVisible
      
      // Close filters popup when clicking outside
      if (this.filtersVisible) {
        setTimeout(() => {
          document.addEventListener('click', this.closeFiltersOnClickOutside)
        }, 0)
      } else {
        document.removeEventListener('click', this.closeFiltersOnClickOutside)
      }
    },
    closeFiltersOnClickOutside(event) {
      const popup = document.querySelector('.side-filters-popup')
      const button = document.querySelector('.filters-btn')
      
      if (popup && !popup.contains(event.target) && !button.contains(event.target)) {
        this.filtersVisible = false
        document.removeEventListener('click', this.closeFiltersOnClickOutside)
      }
    },
    applyFilters() {
      this.$emit('filter-change', {
        month: this.selectedMonth,
        date: this.selectedDate,
        dueDate: this.selectedDueDate
      })
    },
    clearFilters() {
      this.selectedMonth = ''
      this.selectedDate = ''
      this.selectedDueDate = ''
      this.applyFilters()
    }
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeFiltersOnClickOutside)
  }
}
</script>

<style>
.dark-mode .side-menu {
  background-color: #23272f !important;
  color: #f5f5f5 !important;
}
.dark-mode .side-menu h3,
.dark-mode .side-menu .username,
.dark-mode .side-menu button,
.dark-mode .side-menu .icon,
.dark-mode .side-menu .logout-btn {
  color: #f5f5f5 !important;
}
.dark-mode .side-menu button.active {
  background: linear-gradient(135deg, #1976d2, #1565c0) !important;
  color: #fff !important;
}
.dark-mode .side-menu .logout-btn {
  color: #ef5350 !important;
}

.side-menu {
  width: 180px;
  background-color: #ffffff;
  border-right: 1px solid #e0e0e0;
  padding: 20px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.side-menu.dark-mode {
  background-color: #23272f;
  color: #ffffff;
  border-right-color: #333;
}

.user-profile {
  display: flex;
  align-items: center;
  padding: 15px;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.user-profile:hover {
  background-color: #f5f5f5;
}

.dark-mode .user-profile:hover {
  background-color:rgba(27, 79, 52, 0.22);
}

.date{
  width: 87%;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.username {
  font-weight: 500;
}

.side-btn {
  margin-top: 24px;
  width: 100%;
  padding: 10px 0;
  background: #000000;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 1.13em;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 1px 4px rgba(30,40,90,0.08);
  transition: background 0.2s, color 0.2s;
}

.side-btn:hover {
  background:rgb(62, 97, 63);
}

.side-btn.active {
  background: linear-gradient(135deg, #313940, #374452);
  color: #fff;
}

.dark-mode .side-btn {
  background: #1976d2;
  color: #fff;
}

.dark-mode .side-btn.active {
  background: linear-gradient(135deg, #3887fa, #1976d2);
  color: #fff;
}

.filters-btn-wrapper {
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.side-filters-popup {
  position: absolute;
  left: 0;
  right: 0;
  top: 100%;
  margin-top: 8px;
  min-width: 220px;
  background: #f1f1f1;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.13);
  border: 1px solid #e0e0e0;
  padding: 18px 18px 14px 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  z-index: 3000;
}

.side-filters-popup select,
.side-filters-popup input[type="date"] {
  padding: 10px 15px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  color: #222;
  transition: border-color 0.3s, box-shadow 0.3s;
  max-width: 100%;
}

.side-filters-popup select:focus,
.side-filters-popup input[type="date"]:focus {
  border-color: #3887fa;
  outline: none;
  box-shadow: 0 0 0 2px rgba(56, 135, 250, 0.2);
}

/* Fix date input display */
.date-input-wrapper {
  position: relative;
  width: 100%;
}

/* Custom date input styling to match the dark theme */
.dark-mode input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
}

.clear-filters-btn {
  margin-top: 8px;
  padding: 10px;
  background: transparent;
  color: #000000;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-filters-btn:hover {
  background: rgba(44, 49, 56, 0.1);
}

.dark-mode .clear-filters-btn {
  color: #fff;
  border-color: #444;
}

.dark-mode .clear-filters-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.dark-mode .side-filters-popup {
  background: #23272f;
  color: #f5f5f5;
  border: 1px solid #333;
  box-shadow: 0 4px 16px rgba(0,0,0,0.22);
}

.dark-mode .side-filters-popup select,
.dark-mode .side-filters-popup input[type="date"] {
  background-color: #23242a;
  color: #f5f5f5;
  border: 1px solid #444;
}

.filters-btn {
  background: linear-gradient(135deg, #009688,rgb(56, 112, 59));
  color: #fff;
  font-weight: 700;
  font-size: 1.1em;
  border: none;
  border-radius: 10px;
  margin-top: 24px;
  width: 100%;
  padding: 10px 0;
  box-shadow: 0 1px 4px rgba(30,40,90,0.08);
  transition: background 0.2s, color 0.2s;
}
.filters-btn:hover {
  background: linear-gradient(135deg, #43a047, #009688);
}
.dark-mode .filters-btn {
  background: linear-gradient(135deg, #009688,rgb(56, 112, 59));
  color: #fff;
}
.dark-mode .filters-btn:hover {
  background: linear-gradient(135deg, #43a047, #009688);
}
</style>