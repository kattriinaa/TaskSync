<template>
  <div class="task-board">
    <div class="board-content">
      <h1 class="board-title">My Tasks</h1>
      <!-- Горизонтальне меню фільтрів над колонками -->
      <div class="task-type-filters-horizontal">
        <button :class="{active: activeColumnFilter === 'all'}" @click="activeColumnFilter = 'all'">
          All Tasks
        </button>
        <button :class="{active: activeColumnFilter === 'important'}" @click="activeColumnFilter = 'important'">
           Important
        </button>
        <button :class="{active: activeColumnFilter === 'done'}" @click="activeColumnFilter = 'done'">
           Completed
        </button>
      </div>
      <div class="columns-wrapper">
        <div v-if="activeColumnFilter === 'all' || activeColumnFilter === 'todo'" class="column">
          <h2>To Do</h2>
          <div v-if="filteredTodoTasks.length === 0" class="empty-placeholder">No tasks</div>
          <div
            v-for="task in filteredTodoTasks"
            :key="task.id"
            class="task-card"
            :class="{ completed: task.completed, important: task.priority === 'High' }"
            @click="$emit('openTask', task)"
          >
            <h3>{{ task.title }}</h3>
            <p>{{ task.description }}</p>
            <small>Due: {{ formatDate(task.due_date) }}</small>
            <p v-if="task.completed_at">Completed: {{ formatDate(task.completed_at) }}</p>
            <div class="checkbox-container" @click.stop="toggleTaskCompletion(task)">
              <input 
                type="checkbox" 
                v-model="task.completed" 
                @change="updateTaskCompletion(task)" 
              />
            </div>
          </div>
        </div>
        <div v-if="activeColumnFilter === 'all' || activeColumnFilter === 'important'" class="column">
          <h2>Important</h2>
          <div v-if="filteredImportantTasks.length === 0" class="empty-placeholder">No important tasks</div>
          <div
            v-for="task in filteredImportantTasks"
            :key="task.id"
            class="task-card"
            :class="{ completed: task.completed, important: task.priority === 'High' }"
            @click="$emit('openTask', task)"
          >
            <h3>{{ task.title }}</h3>
            <p>{{ task.description }}</p>
            <small>Due: {{ formatDate(task.due_date) }}</small>
            <p v-if="task.completed_at">Completed: {{ formatDate(task.completed_at) }}</p>
            <div class="checkbox-container" @click.stop="toggleTaskCompletion(task)">
              <input 
                type="checkbox" 
                v-model="task.completed" 
                @change="updateTaskCompletion(task)" 
              />
            </div>
          </div>
        </div>
        <div v-if="activeColumnFilter === 'all' || activeColumnFilter === 'done'" class="column">
          <h2>Done</h2>
          <div v-if="filteredDoneTasks.length === 0" class="empty-placeholder">No completed tasks</div>
          <div
            v-for="task in filteredDoneTasks"
            :key="task.id"
            class="task-card"
            :class="{ completed: task.completed, important: task.priority === 'High' }"
            @click="$emit('openTask', task)"
          >
            <h3>{{ task.title }}</h3>
            <p>{{ task.description }}</p>
            <p v-if="task.completed_at"><strong>Completed:</strong> {{ formatDate(task.completed_at) }}</p>
            <div 
              v-if="!task.completed" 
              class="checkbox-container" 
              @click.stop="toggleTaskCompletion(task)"
            >
              <input 
                type="checkbox" 
                v-model="task.completed" 
                @change="updateTaskCompletion(task)" 
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { format } from 'date-fns';

export default {
  props: {
    tasks: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      filterDueDate: '', // Фільтр за датою
      filterMonth: '', // Фільтр по місяцю
      filterDate: '', // Введення конкретної дати
      filtersVisible: false,  // Перемикання видимості фільтрів
      months: [
        { value: '01', name: 'January' },
        { value: '02', name: 'February' },
        { value: '03', name: 'March' },
        { value: '04', name: 'April' },
        { value: '05', name: 'May' },
        { value: '06', name: 'June' },
        { value: '07', name: 'July' },
        { value: '08', name: 'August' },
        { value: '09', name: 'September' },
        { value: '10', name: 'October' },
        { value: '11', name: 'November' },
        { value: '12', name: 'December' },
      ],
      activeColumnFilter: 'all',
    };
  },
  computed: {
    filteredTodoTasks() {
      return this.tasks
        .filter(task => {
          return !task.completed && task.priority !== 'High' && this.applyFilters(task);
        })
        .sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
    },
    filteredImportantTasks() {
      return this.tasks
        .filter(task => {
          return task.priority === 'High' && !task.completed && this.applyFilters(task);
        })
        .sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
    },
    filteredDoneTasks() {
      return this.tasks
        .filter(task => {
          return task.completed && this.applyFilters(task);
        })
        .sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
    },
  },
  methods: {
    applyFilters(task) {
      const today = new Date();
      const taskDueDate = new Date(task.due_date);

      // Фільтрація за конкретною датою
      if (this.filterDate && taskDueDate.toDateString() !== new Date(this.filterDate).toDateString()) {
        return false;
      }

      // Фільтрація за місяцем
      if (this.filterMonth && taskDueDate.getMonth() + 1 !== parseInt(this.filterMonth)) {
        return false;
      }

      // Фільтрація за іншими умовами (сьогодні, завтра, наступний тиждень)
      if (this.filterDueDate) {
        if (this.filterDueDate === 'today' && taskDueDate.toDateString() !== today.toDateString()) return false;
        if (this.filterDueDate === 'tomorrow') {
          const tomorrow = new Date(today);
          tomorrow.setDate(today.getDate() + 1);
          if (taskDueDate.toDateString() !== tomorrow.toDateString()) return false;
        }
        if (this.filterDueDate === 'nextWeek') {
          const nextWeek = new Date(today);
          nextWeek.setDate(today.getDate() + 7);
          if (taskDueDate.getTime() > nextWeek.getTime()) return false;
        }
      }

      return true;
    },
    toggleFilters() {
      this.filtersVisible = !this.filtersVisible;
      console.log('toggleFilters called, filtersVisible:', this.filtersVisible);
    },
    toggleTaskCompletion(task) {
      task.completed = !task.completed;
      if (task.completed) {
        task.completed_at = new Date().toISOString(); // Встановлюємо дату виконання
        this.$emit('completed', task);
      } else {
        task.completed_at = null; // Скидаємо дату виконання
      }
      this.updateTaskCompletion(task);
    },
    async updateTaskCompletion(task) {
      try {
        const response = await axios.put(`/api/tasks/${task.id}`, { 
          completed: task.completed, 
          completed_at: task.completed_at 
        });
        console.log("Завдання оновлено:", response.data);
        task.completed = response.data.completed;
        task.completed_at = response.data.completed_at;
      } catch (error) {
        console.error("Не вдалося оновити завдання:", error);
      }
    },
    formatDate(date) {
      return format(new Date(date), 'yyyy-MM-dd');
    },
  },
};
</script>

<style>
.dark-mode .column {
  background: #23272f;
  border-radius: 16px;
  border: 1.5px solid #2e3a40;
  box-shadow: 0 4px 12px rgba(0,0,0,0.18);
}
.dark-mode .column *,
.dark-mode .task-card {
  color: #f5f5f5 !important;
}
.dark-mode .task-card {
  background: linear-gradient(145deg, #23272f, #181a20) !important;
  color: #f5f5f5 !important;
  box-shadow: 0 4px 10px rgba(52, 50, 50, 0.44);
  border: 2px solid rgb(44, 49, 45) !important;
}

.dark-mode .task-card.completed {
  background: linear-gradient(145deg, #23382f, #1a2a20) !important;
  color: #d0ffd0 !important;
}
.dark-mode .task-card.important {
  border: 2px solid #ffd600 !important;
  box-shadow: 0 4px 12px rgba(255, 214, 0, 0.15) !important;
}
.dark-mode .task-type-filters button {
  background:rgb(0, 0, 0) !important;
  color: #fff !important;
  border: none !important;
}
.dark-mode .task-type-filters button.active {
  background: linear-gradient(135deg, #009688, #43a047) !important;
  color: #fff !important;
}

.board-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding-left: 0;
  padding-right: 0;
  background: none;
  box-shadow: none;
}
.board-title {
  margin-top: 32px;
  margin-bottom: 0;
  font-size: 2.5em;
  font-weight: bold;
  color: #222;
  text-align: left;
}
.dark-mode .board-title {
  color: #ffffff !important;
}
.task-type-filters-horizontal {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 14px;
  margin: 24px 0 24px 0;
  width: 100%;
  max-width: 700px;
  text-align: left;
}

/* General light mode */
.task-type-filters-horizontal button {
  background: #f5f5f5;
  color: #222;
  border: none;
  border-radius: 20px;
  padding: 12px 24px;
  font-size: 1em;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  box-shadow: 0 2px 8px rgb(28, 54, 14);
}
.task-type-filters-horizontal button.active {
  background: #009688 !important;
  background: linear-gradient(135deg, #009688, #43a047);
  color: #fff;
  box-shadow: 0 4px 16px rgba(0,123,255,0.10);
}
.task-type-filters-horizontal .icon {
  font-size: 1.2em;
}
.task-type-filters-horizontal button.active {
  background: linear-gradient(135deg, #009688, #43a047);
  color: #fff;
}

/* Dark mode override */
.dark-mode .task-type-filters-horizontal button {
  background: #1b1b1b !important;
  color: #f5f5f5 !important;
}
.dark-mode .task-type-filters-horizontal button.active {
  background: linear-gradient(135deg, #009688, #43a047) !important;
  color: #fff !important;
}
@media (max-width: 1200px) {
  .board-content {
    max-width: 100%;
    margin-left: 10px;
    margin-right: 10px;
  }
  .columns-wrapper {
    gap: 18px;
  }
  .column {
    width: 100%;
    min-width: 180px;
    max-width: 100%;
    padding: 10px;
  }
}
@media (max-width: 700px) {
  .columns-wrapper {
    flex-direction: column;
    gap: 18px;
    align-items: stretch;
    justify-content: flex-start;
  }
  .column {
    width: 100%;
    min-width: 0;
    max-width: 100%;
    padding: 8px;
  }
}

/* Стилі для контейнера фільтрів */
.filters-container {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  position: relative;
  overflow: visible;
  min-height: 60px;
}

/* Стиль кнопки для відкриття фільтрів */
.filters-toggle {
  position: relative;
  z-index: 2100;
  background: linear-gradient(135deg, #007bff, #06294f);
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 25px;
  transition: background-color 0.3s;
}

.filters-toggle:hover {
  background: linear-gradient(135deg, #0056b3, #06294f);
}

/* Основні стилі для блоку фільтрів */
.filters {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 15px;
  padding: 10px 15px;
  background-color: #f1f1f1;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.13);
  max-width: 95vw;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 100%;
  z-index: 2000;
  border: 1px solid #e0e0e0;
  width: auto;
  margin-top: 8px;
  overflow-x: auto;
}
.filters::after {
  content: '';
  position: absolute;
  left: 50%;
  top: -10px;
  transform: translateX(-50%);
  border-width: 0 10px 10px 10px;
  border-style: solid;
  border-color: transparent transparent #f1f1f1 transparent;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.10));
}
.dark-mode .filters {
  background-color: #23272f;
  color: #f5f5f5;
  border: 1px solid #333;
  box-shadow: 0 4px 16px rgba(0,0,0,0.22);
}
.dark-mode .filters::after {
  border-color: transparent transparent #23272f transparent;
}
.filters select,
.filters input[type="date"] {
  padding: 10px 15px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  color: #222;
  transition: border-color 0.3s, box-shadow 0.3s;
  width: 100%;
  max-width: 100%;
}
.dark-mode .filters select,
.dark-mode .filters input[type="date"] {
  background-color: #23242a;
  color:rgb(60, 60, 60);
  border: 1px solid #444;
}

/* Зміна кольору бордеру при фокусуванні */
.filters select:focus,
.filters input[type="date"]:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* Стилі для option в селектах */
.filters select option {
  padding: 10px;
  font-size: 16px;
}

/* Зміна фону для option при наведенні */
.filters select option:hover {
  background-color: #f1f1f1;
}

/* Основні стилі для дошки завдань */
.task-board {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 20px;
  width: 100%;
  max-width: 100vw;
  min-width: 0;
  min-height: calc(100vh - 80px);
  box-sizing: border-box;
  align-items: flex-start;
  flex-wrap: wrap;
  overflow-x: auto;
}

/* Стилі для кожного стовпця */
.column {
  background: #fff;
  color: #222;
  border: 1.5px solid #e0e0e0;
  box-shadow: 0 4px 12px rgba(30,40,90,0.06);
  border-radius: 16px;
  padding: 18px 12px 24px 12px;
  min-width: 260px;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  gap: 15px;
  box-sizing: border-box;
  overflow: visible;
  align-items: stretch;
}
.dark-mode .column {
  background: #23272f;
  color: #fff;
  border: 1.5px solid #2e3a40;
  box-shadow: 0 4px 16px rgba(30,40,90,0.10);
}

/* Заголовки стовпців */
.column h2 {
  text-align: center;
  font-size: 1.3em;
  font-weight: bold;
  color: #fff;
  margin-bottom: 15px;
  letter-spacing: 0.5px;
}

/* Картка завдання */
.task-card {
  position: relative;
  padding: 15px;
  background: linear-gradient(145deg, #fff, #f7f9fa);
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(30,40,90,0.06);
  margin-bottom: 15px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  color: #222;
}

.task-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

/* Стилі для виконаних завдань */
.task-card.completed {
  background: linear-gradient(145deg, #e8f5e9, #f1f8e9);
  color: #388e3c;
}

/* Стилі для важливих завдань */
.task-card.important {
  border: 2px solid #ffd600;
  box-shadow: 0 4px 12px rgba(255, 214, 0, 0.13);
}

/* Стилі для галочки */
.checkbox-container {
  position: absolute;
  bottom: 10px;
  right: 10px;
  cursor: pointer;
  visibility: hidden;
}

.task-card:hover .checkbox-container {
  visibility: visible;
}

.checkbox-container input[type="checkbox"] {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  appearance: none;
  border: 2px solid #009688;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.checkbox-container input[type="checkbox"]:checked {
  background: linear-gradient(135deg, #009688, #43a047);
  border-color: #009688;
}

.checkbox-container input[type="checkbox"]:checked::before {
  content: '✔';
  position: absolute;
  top: 3px;
  left: 6px;
  font-size: 14px;
  color: white;
}

/* Адаптивність для мобільних пристроїв */
@media (max-width: 1100px) {
  .board-content {
    margin-left: 10px;
    margin-right: 10px;
  }
  .columns-wrapper {
    gap: 12px;
  }
  .column {
    min-width: 180px;
    padding: 10px;
  }
}
.columns-wrapper {
  display: flex;
  flex-direction: row;
  gap: 20px;
  align-items: flex-start;
  justify-content: center;
  width: 100%;
  margin-top: 24px;
  overflow-x: auto;
  min-width: 0;
  box-sizing: border-box;
  flex-wrap: wrap;
}
.column {
  flex: 1 1 0;
  background: #23272f;
  border-radius: 16px;
  padding: 18px 12px 24px 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  min-width: 260px;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  gap: 15px;
  box-sizing: border-box;
  overflow: visible;
  color: #fff;
  align-items: stretch;
}
.column h2 {
  text-align: center;
  font-size: 1.3em;
  font-weight: bold;
  color: #fff;
  margin-bottom: 15px;
  letter-spacing: 0.5px;
}
.light-mode .column {
  background: #fff;
  color: #222;
  border: 1.5px solid #e0e0e0;
  box-shadow: 0 4px 12px rgba(30,40,90,0.06);
}
.light-mode .column h2 {
  color: #222;
}
.task-card {
  position: relative;
  padding: 15px;
  background: linear-gradient(145deg, #fff, #f7f9fa);
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(30,40,90,0.06);
  margin-bottom: 15px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  color: #222;
}
.task-card.completed {
  color: #388e3c;
}
.task-card.important {
  border: 2px solid #ffd600;
  box-shadow: 0 4px 12px rgba(255, 214, 0, 0.13);
}
.empty-placeholder {
  text-align: center;
  color: #aaa;
  font-size: 1.1em;
  margin: 30px 0;
}
.light-mode .board-content {
  background: none;
  box-shadow: none;
}
</style>