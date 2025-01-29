<template>
  <div class="task-board">
    <!-- Кнопка для фільтрів -->
    <div class="filters-container">
      <button class="filters-toggle" @click="toggleFilters">
        Filters
      </button>

      <div v-if="filtersVisible" class="filters">

        <select v-model="filterDueDate">
          <option value="">All Dates</option>
          <option value="today">Today</option>
          <option value="tomorrow">Tomorrow</option>
          <option value="nextWeek">Next Week</option>
        </select>
      </div>
    </div>

    <!-- Стовпці для завдань -->
    <div class="column">
      <h2>To Do</h2>
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

    <div class="column">
      <h2>Important</h2>
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
        <!-- Виведення дати виконання -->
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

    <div class="column">
      <h2>Done</h2>
      <div
        v-for="task in filteredDoneTasks"
        :key="task.id"
        class="task-card"
        :class="{ completed: task.completed, important: task.priority === 'High' }"
        @click="$emit('openTask', task)"
      >
        <h3>{{ task.title }}</h3>
        <p>{{ task.description }}</p>

        <!-- Замінили на окремі рядки -->
        <p><strong>Due:</strong> {{ formatDate(task.due_date) }}</p>
        <p v-if="task.completed_at"><strong>Completed:</strong> {{ formatDate(task.completed_at) }}</p>

        <div class="checkbox-container" @click.stop="toggleTaskCompletion(task)">
          <input 
            type="checkbox" 
            v-model="task.completed" 
            @change="updateTaskCompletion(task)" 
          />
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
      filtersVisible: false,  // Перемикання видимості фільтрів
    };
  },
  computed: {
  filteredTodoTasks() {
    return this.tasks
      .filter(task => {
        return !task.completed && task.priority !== 'High' && this.applyFilters(task);
      })
      .sort((a, b) => new Date(a.due_date) - new Date(b.due_date));  // Сортування по даті
  },
  filteredImportantTasks() {
    return this.tasks
      .filter(task => {
        return task.priority === 'High' && !task.completed && this.applyFilters(task);
      })
      .sort((a, b) => new Date(a.due_date) - new Date(b.due_date));  // Сортування по даті
  },
  filteredDoneTasks() {
    return this.tasks
      .filter(task => {
        return task.completed && this.applyFilters(task);
      })
      .sort((a, b) => new Date(a.due_date) - new Date(b.due_date));  // Сортування по даті
  },
},
  methods: {
    applyFilters(task) {
      

      // Фільтрація за датою
      if (this.filterDueDate) {
        const today = new Date();
        const taskDueDate = new Date(task.due_date);
        
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
    },
    toggleTaskCompletion(task) {
      task.completed = !task.completed;
      if (task.completed) {
        task.completed_at = new Date().toISOString(); // Встановлюємо дату виконання
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
        task.completed = response.data.completed;  // Оновлення статусу локально
        task.completed_at = response.data.completed_at; // Оновлення дати виконання
      } catch (error) {
        console.error("Не вдалося оновити завдання:", error);
      }
    },
    formatDate(date) {
      return format(new Date(date), 'yyyy-MM-dd'); // Перетворення в формат "2025-01-28"
    },
  },
};
</script>

<style scoped>
/* Стилі для фільтрів */
.filters-container {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.filters-toggle {
  background: linear-gradient(135deg, #007bff, #06294f);
  color: white;
  border: none;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 10px;
  transition: background-color 0.3s;
}

.filters-toggle:hover {
  background: linear-gradient(135deg, #0056b3, #06294f);
}

.filters {
  display: flex;
  gap: 20px;
}

.filters select {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

/* Основні стилі для дошки завдань */
.task-board {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 20px;
  width: calc(100vw - 60px); /* Враховує простір для кнопок */
  min-height: calc(100vh - 80px); /* Мінімальна висота для адаптації контенту */
  box-sizing: border-box; /* Враховує padding у розмірах */
  align-items: flex-start; /* Стовпці вирівняні по верху */
}

/* Стилі для кожного стовпця */
.column {
  flex: 1; /* Рівномірний розподіл ширини */
  background-color: #f8f9fa;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 280px; /* Мінімальна ширина */
  display: flex;
  flex-direction: column;
  gap: 15px;
  box-sizing: border-box; /* Враховує padding */
  overflow: visible; /* Вміст не обрізається */
}

/* Заголовки стовпців */
.column h2 {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
}

/* Картка завдання */
.task-card {
  position: relative;
  padding: 15px;
  background: linear-gradient(145deg, #ffffff, #f1f1f1);
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.task-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

/* Стилі для виконаних завдань */
.task-card.completed {
  background: linear-gradient(145deg, #dff8e1, #cce6d7);
}

/* Стилі для важливих завдань */
.task-card.important {
  border: 2px solid #ffc107;
  box-shadow: 0 4px 12px rgba(255, 193, 7, 0.3);
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
  border: 2px solid #007bff;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.checkbox-container input[type="checkbox"]:checked {
  background: linear-gradient(135deg, #007bff, #2575fc);
  border-color: #2575fc;
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
@media (max-width: 768px) {
  .filters-container {
    flex-direction: column;
  }

  .filters {
    flex-direction: column;
    gap: 10px;
    width: 100%;
  }

  .filters-toggle {
    width: 100%;
  }
}
</style>
