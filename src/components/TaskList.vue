<template>
  <div class="task-board">
    <!-- Стовпці для завдань -->
    <div class="column">
      <h2>Do</h2>
      <div
        v-for="task in todoTasks"
        :key="task.id"
        class="task-card"
        :class="{ completed: task.completed, important: task.priority === 'High' }"
        @click="$emit('openTask', task)"
      >
        <h3>{{ task.title }}</h3>
        <p>{{ task.description }}</p>
        <small>Дата: {{ task.due_date }}</small>

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
        v-for="task in importantTasks"
        :key="task.id"
        class="task-card"
        :class="{ completed: task.completed, important: task.priority === 'High' }"
        @click="$emit('openTask', task)"
      >
        <h3>{{ task.title }}</h3>
        <p>{{ task.description }}</p>
        <small>Дата: {{ task.due_date }}</small>

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
        v-for="task in doneTasks"
        :key="task.id"
        class="task-card"
        :class="{ completed: task.completed, important: task.priority === 'High' }"
        @click="$emit('openTask', task)"
      >
        <h3>{{ task.title }}</h3>
        <p>{{ task.description }}</p>
        <small>Дата: {{ task.due_date }}</small>

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

export default {
  props: {
    tasks: {
      type: Array,
      required: true,
    },
  },
  computed: {
    todoTasks() {
      return this.tasks.filter((task) => !task.completed && task.priority !== 'High');
    },
    importantTasks() {
      return this.tasks.filter((task) => task.priority === 'High' && !task.completed);
    },
    doneTasks() {
      return this.tasks.filter((task) => task.completed);
    },
  },
  methods: {
  toggleTaskCompletion(task) {
    task.completed = !task.completed;
    this.updateTaskCompletion(task);
  },
  
  async updateTaskCompletion(task) {
  try {
    const response = await axios.put(`/api/tasks/${task.id}`, { completed: task.completed
    });
    console.log("Завдання оновлено:", response.data);
    task.completed = response.data.completed;  // Оновлення статусу локально
  } catch (error) {
    console.error("Не вдалося оновити завдання:", error);
  }
}
},
};
</script>

<style scoped>
/* Глобальні стилі для body або html для прокрутки */
html, body {
  margin: 0;
  padding: 0;
  overflow-x: hidden; /* Приховує горизонтальну прокрутку */
  overflow-y: auto; /* Дозволяє вертикальну прокрутку */
  width: 100%;
  height: 100%;
  box-sizing: border-box; /* Враховує padding у розмірах */
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
</style>
