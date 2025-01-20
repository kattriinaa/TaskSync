<template>
  <div id="app">
    <!-- Кнопка Logout -->
    <button v-if="isAuthenticated" class="logout-btn" @click="logout">Logout</button>

    <!-- Реєстраційна/логін форма -->
    <div v-if="!isAuthenticated" class="login-container">
      <h1>Login to TaskSync</h1>
      <form @submit.prevent="login">
        <input type="text" v-model="credentials.username" placeholder="Username" required />
        <input type="password" v-model="credentials.password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
    </div>

    <!-- Основний інтерфейс -->
    <div v-else class="main-container">
      <!-- Меню зліва -->
      <aside class="sidebar">
        <h2>Фільтри</h2>
        <ul>
          <li @click="filterTasks('all')">Всі</li>
          <li @click="filterTasks('important')">Важливі</li>
          <li @click="filterTasks('completed')">Виконані</li>
        </ul>
      </aside>

      <!-- Основний контент -->
      <main class="content">
        <h1>TaskSync</h1>

        <!-- Кнопка "Додати задачу" -->
        <button class="add-task-btn" @click="showAddTaskModal">Додати задачу</button>

        <!-- Список задач -->
        <div class="task-list">
          <div
            v-for="task in filteredTasks"
            :key="task.id"
            class="task-card"
            :class="{ completed: task.completed, important: task.priority === 'High' }"
            @click="openTask(task)"
          >
            <h3>{{ task.title }}</h3>
            <p>{{ task.description }}</p>
            <small>Дата: {{ task.due_date }}</small>
          </div>
        </div>
      </main>
    </div>

    <!-- Модальне вікно для додавання задачі -->
    <div v-if="showAddModal" class="modal">
      <div class="modal-content">
        <h2>Нова задача</h2>
        <form @submit.prevent="addTask">
          <input type="text" v-model="newTask.title" placeholder="Заголовок" required />
          <textarea v-model="newTask.description" placeholder="Опис"></textarea>
          <input type="date" v-model="newTask.due_date" required />
          <select v-model="newTask.priority">
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
          <button type="submit">Додати</button>
          <button type="button" @click="closeAddTaskModal">Закрити</button>
        </form>
      </div>
    </div>

    <!-- Модальне вікно для перегляду задачі -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h2>Деталі задачі</h2>
        <form @submit.prevent="editTask">
          <input type="text" v-model="selectedTask.title" placeholder="Заголовок" required />
          <textarea v-model="selectedTask.description" placeholder="Опис"></textarea>
          <input type="date" v-model="selectedTask.due_date" required />
          <select v-model="selectedTask.priority">
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
          <button type="submit">Зберегти</button>
          <button type="button" @click="closeEditTaskModal">Закрити</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isAuthenticated: false, // Стан авторизації
      credentials: { username: '', password: '' }, // Дані для логіну
      tasks: [], // Всі задачі
      filteredTasks: [], // Відфільтровані задачі
      showAddModal: false, // Відображення модального вікна для додавання задачі
      showEditModal: false, // Відображення модального вікна для перегляду задачі
      newTask: { title: '', description: '', due_date: '', priority: 'Low' }, // Нова задача
      selectedTask: null // Обрана задача для перегляду/редагування
    };
  },
  methods: {
    login() {
      if (this.credentials.username === 'kattrina' && this.credentials.password === 'tasksyncc') {
        this.isAuthenticated = true;
        localStorage.setItem('isAuthenticated', 'true'); // Зберігаємо статус авторизації
        this.fetchTasks();
      } else {
        alert('Invalid username or password');
      }
    },
    logout() {
      this.isAuthenticated = false;
      localStorage.removeItem('isAuthenticated');
      this.credentials = { username: '', password: '' };
    },
    filterTasks(filter) {
      if (filter === 'all') {
        this.filteredTasks = this.tasks;
      } else if (filter === 'important') {
        this.filteredTasks = this.tasks.filter(task => task.priority === 'High');
      } else if (filter === 'completed') {
        this.filteredTasks = this.tasks.filter(task => task.completed);
      }
    },
    fetchTasks() {
      this.tasks = [
        { id: 1, title: 'Приклад задачі 1', description: 'Опис 1', due_date: '2025-01-20', priority: 'Medium', completed: false },
        { id: 2, title: 'Приклад задачі 2', description: 'Опис 2', due_date: '2025-01-22', priority: 'High', completed: true }
      ];
      this.filterTasks('all');
    },
    showAddTaskModal() {
      this.showAddModal = true;
    },
    closeAddTaskModal() {
      this.showAddModal = false;
    },
    addTask() {
      this.tasks.push({ ...this.newTask, id: Date.now(), completed: false });
      this.filterTasks('all');
      this.closeAddTaskModal();
    },
    openTask(task) {
      this.selectedTask = { ...task };
      this.showEditModal = true;
    },
    closeEditTaskModal() {
      this.showEditModal = false;
    },
    editTask() {
      const index = this.tasks.findIndex(task => task.id === this.selectedTask.id);
      if (index !== -1) {
        this.tasks[index] = { ...this.selectedTask };
      }
      this.filterTasks('all');
      this.closeEditTaskModal();
    }
  },
  mounted() {
    const authStatus = localStorage.getItem('isAuthenticated');
    if (authStatus === 'true') {
      this.isAuthenticated = true;
      this.fetchTasks();
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

.main-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

h1 {
  color: #343a40;
}

.add-task-btn {
  position: absolute;
  top: 20px;
  right: 150px;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.add-task-btn:hover {
  background-color: #0056b3;
}

.task-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 20px;
  justify-content: center;
}

.task-card {
  width: 250px;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.task-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.task-card.completed {
  background-color: #d4edda;
}

.task-card.important {
  border: 2px solid #ffc107;
}

.logout-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.logout-btn:hover {
  background-color: #c82333;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6); /* Тінь фону */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 12px;
  width: 400px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); /* Тінь для модального вікна */
  text-align: center;
  position: relative;
}

.modal-content h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #343a40;
}

.modal-content form {
  display: flex;
  flex-direction: column;
}

.modal-content input,
.modal-content textarea,
.modal-content select {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: Arial, sans-serif;
}

.modal-content textarea {
  height: 80px;
  resize: none; /* Забороняє зміну розміру текстового поля */
}

.modal-content button {
  padding: 10px 15px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}

.modal-content button[type="submit"] {
  background-color: #007bff;
  color: white;
}

.modal-content button[type="submit"]:hover {
  background-color: #0056b3;
}

.modal-content button[type="button"] {
  background-color: #dc3545;
  color: white;
  margin-top: 10px;
}

.modal-content button[type="button"]:hover {
  background-color: #c82333;
}

/* Анімація модального вікна */
@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-content {
  animation: modalFadeIn 0.3s ease-out;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
  text-align: center;
}

h1 {
  color: #007bff;
  margin-top: 20px;
}

h2 {
  color: #555;
  margin: 20px 0;
}

form {
  max-width: 300px;
  margin: 0 auto;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

form input,
form select {
  width: calc(100% - 20px);
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

form button {
  width: 100%;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
}

form button:hover {
  background-color: #0056b3;
}

ul {
  list-style: none;
  padding: 0;
  max-width: 600px;
  margin: 20px auto;
}

ul li {
  background-color: white;
  padding: 15px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #c82333;
}

.logout-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.logout-btn:hover {
  background-color: #c82333;
}
</style>