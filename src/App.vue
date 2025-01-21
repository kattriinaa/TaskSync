<template>
  <div id="app">
    <LoginForm v-if="!isAuthenticated" @login="handleLogin" />

    <div v-else class="main-container">
      <button class="logout-btn" @click="logout">Вийти</button>
      <TaskSidebar :filter="filterTasks" />
      <div class="task-content">
        <TaskList 
          :tasks="filteredTasks" 
          @openTask="openTask"
          @showAddModal="showAddTaskModal"
        />
        <TaskModal
          v-if="showModal"
          :task="currentTask"
          :mode="modalMode"
          @save="saveTask"
          @delete="deleteTask"
          @close="closeModal"
        />
      </div>
      <button class="add-task-btn" @click="showAddTaskModal">+</button>
    </div>
  </div>
</template>

<script>
import LoginForm from './components/LoginForm.vue';
import TaskSidebar from './components/TaskSidebar.vue';
import TaskList from './components/TaskList.vue';
import TaskModal from './components/TaskModal.vue';

export default {
  components: { LoginForm, TaskSidebar, TaskList, TaskModal },
  data() {
    return {
      isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
      tasks: [],
      filteredTasks: [],
      showModal: false,
      currentTask: null,
      modalMode: 'add',
    };
  },
 methods: {
    handleLogin(credentials) {
      if (credentials.username === "kattrina" && credentials.password === "tasksyncc") {
        this.isAuthenticated = true;
        localStorage.setItem("isAuthenticated", "true");
        this.fetchTasks();
      } else {
        alert("Invalid credentials");
      }
    },
    fetchTasks() {
      this.tasks = [
        { id: 1, title: "Task 1", description: "Description 1", due_date: "2025-01-25", priority: "Medium", completed: false },
        { id: 2, title: "Task 2", description: "Description 2", due_date: "2025-01-26", priority: "High", completed: true },
      ];
      this.filteredTasks = this.tasks;
    },
    filterTasks(filter) {
      if (filter === "all") {
        this.filteredTasks = this.tasks;
      } else if (filter === "important") {
        this.filteredTasks = this.tasks.filter(task => task.priority === "High");
      } else if (filter === "completed") {
        this.filteredTasks = this.tasks.filter(task => task.completed);
      }
    },
    openTask(task) {
      this.currentTask = { ...task };
      this.showModal = true;
      this.modalMode = "edit";
    },
    showAddTaskModal() {
      this.currentTask = { title: "", description: "", due_date: "", priority: "Low" };
      this.showModal = true;
      this.modalMode = "add";
    },
    saveTask(task) {
      if (this.modalMode === "add") {
        this.tasks.push({ ...task, id: Date.now(), completed: false });
      } else {
        const index = this.tasks.findIndex(t => t.id === task.id);
        if (index !== -1) {
          this.tasks.splice(index, 1, task);
        }
      }
      this.filteredTasks = this.tasks;
      this.showModal = false;
    },
    deleteTask(task) {
      this.tasks = this.tasks.filter(t => t.id !== task.id);
      this.filteredTasks = this.tasks;
      this.showModal = false;
    },
    closeModal() {
      this.showModal = false;
    },
},
  mounted() {
    this.fetchTasks();
  },
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f4f4;
}

.main-container {
  display: flex;
}

.task-content {
  margin-left: 260px;
  padding: 20px;
  flex-grow: 1;
}

.add-task-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background-color: #007bff;
  color: white;
  border: none;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.add-task-btn:hover {
  background-color: #0056b3;
}

.logout-btn {
  position: fixed;
  top: 10px;
  right: 10px;
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.logout-btn:hover {
  background-color: #c82333;
}
</style>