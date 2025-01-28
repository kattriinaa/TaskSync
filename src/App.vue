
<template>
  <div id="app">
    <!-- Компонент LoginForm, який показується, якщо користувач не автентифікований -->
    <LoginForm v-if="!isAuthenticated" @login="handleLogin"></LoginForm>

    <!-- Головний екран -->
    <div v-else>
      <!-- Екран вітання -->
      <div v-if="!hasVisited" class="welcome-screen">
        <h1>Welcome to TaskSync!</h1>
        <p>TaskSync is your perfect planner for organizing tasks and syncing with Trello.</p>
        <button class="welcome-btn" @click="closeWelcome">Go to Planner</button>
      </div>

      <!-- Основний контент після вітання -->
      <div v-else class="main-container">
        <!-- Кнопка меню з трьома рисочками -->
        <button class="menu-btn" @click="toggleMenu">
          &#9776;
        </button>

        <!-- Кнопки меню -->
        <div v-if="isMenuVisible" class="menu-options" ref="menu">
          <button class="logout-btn" @click="logout">Logout</button>
          <button class="sync-btn" @click="fetchTrelloTasks('6791532692984e03de85b23f')">
            Sync with Trello
          </button>
        </div>

        <!-- Список завдань -->
        <div class="task-content">
          <TaskList
            :tasks="filteredTasks"
            :filterCriteria="filterCriteria"
            @openTask="openTask"
            @showAddModal="showAddTaskModal"
            @close="closeModal"
          />
          <TaskModal
            v-if="showModal"
            :task="currentTask || { title: '', description: '', due_date: '', priority: '', syncToTrello: false }"
            :mode="modalMode"
            @save="saveTask"
            @delete="deleteTask"
            @close="closeModal"
          />
        </div>

        <!-- Кнопка додавання завдання -->
        <button class="add-task-btn" @click="showAddTaskModal">+</button>
      </div>
    </div>
  </div>
</template>

<script>
import LoginForm from './components/LoginForm.vue';
import TaskList from './components/TaskList.vue';
import TaskModal from './components/TaskModal.vue';

export default {
  components: { LoginForm, TaskList, TaskModal },
  data() {
    return {
      isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
      hasVisited: localStorage.getItem('hasVisited') === 'true', // Check if the user has visited the planner before
      tasks: [],
      filteredTasks: [],
      showModal: false,
      currentTask: null,
      modalMode: 'add',
      isMenuVisible: false,
      filterCriteria: {},
    };
  },
  methods: {
    handleLogin() {
      this.isAuthenticated = true;
      localStorage.setItem('isAuthenticated', 'true');
      this.fetchTasks();
      this.fetchTrelloTasks();
      this.hasVisited = false; // Reset hasVisited so the welcome screen shows after login
      localStorage.removeItem('hasVisited'); // Clear the previous "hasVisited" state
    },

    toggleMenu(event) {
      this.isMenuVisible = !this.isMenuVisible;
      event.stopPropagation();
    },

    logout() {
      this.isAuthenticated = false;
      localStorage.removeItem('isAuthenticated');
      this.hasVisited = false; // Ensure that after logout, welcome screen shows again
      localStorage.removeItem('hasVisited');
    },

    closeWelcome() {
      this.hasVisited = true;
      localStorage.setItem('hasVisited', 'true');
    },

    showAddTaskModal() {
      this.modalMode = 'add';
      this.currentTask = null;
      this.showModal = true;
    },

    openTask(task) {
      this.modalMode = 'edit';
      this.currentTask = task;
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
    },

    async fetchTasks() {
      try {
        const response = await fetch('/api/tasks');
        if (!response.ok) throw new Error('Failed to fetch tasks');
        this.tasks = await response.json();
        this.filteredTasks = this.tasks;
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    },

    async saveTask(task) {
      try {
        let response, newTask;

        if (this.modalMode === 'add') {
          response = await fetch('/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(task),
          });

          if (!response.ok) throw new Error('Failed to add task');

          newTask = await response.json();
          this.tasks.push(newTask);

          if (task.syncToTrello) {
            await this.syncTaskToTrello(newTask);
          }
        } else {
          response = await fetch(`/api/tasks/${task.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(task),
          });

          if (!response.ok) throw new Error('Failed to update task');

          const index = this.tasks.findIndex(t => t.id === task.id);
          if (index !== -1) this.tasks.splice(index, 1, task);
        }

        this.filteredTasks = this.tasks;
        this.showModal = false;
      } catch (error) {
        console.error('Error saving task:', error);
      }
    },

    async deleteTask(task) {
      try {
        await fetch(`/api/tasks/${task.id}`, { method: 'DELETE' });
        this.tasks = this.tasks.filter(t => t.id !== task.id);
        this.filteredTasks = this.tasks;
        this.showModal = false;
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    },

    filterTasks(filterType) {
      if (filterType === 'all') {
        this.filteredTasks = this.tasks;
      } else if (filterType === 'important') {
        this.filteredTasks = this.tasks.filter(task => task.priority === 'High');
      } else if (filterType === 'completed') {
        this.filteredTasks = this.tasks.filter(task => task.completed);
      }
    },

    async fetchTrelloTasks(listId) {
      try {
        const response = await fetch(`/api/trello/tasks/${listId}`);
        if (!response.ok) throw new Error('Failed to fetch tasks from Trello');

        const trelloTasks = await response.json();
        const formattedTasks = trelloTasks.map(trelloTask => ({
          id: trelloTask.id,
          title: trelloTask.name,
          description: trelloTask.desc || '',
          due_date: trelloTask.due || null,
          priority: 'Medium',
        }));

        this.tasks = [
          ...this.tasks.filter(task => !formattedTasks.some(newTask => newTask.id === task.id)),
          ...formattedTasks
        ];
        this.filteredTasks = this.tasks;
      } catch (error) {
        console.error('Error syncing tasks from Trello:', error);
      }

      this.isMenuVisible = false;
    },

    closeMenuOnOutsideClick(event) {
      const menu = this.$refs.menu;
      if (menu && !menu.contains(event.target) && this.isMenuVisible) {
        this.isMenuVisible = false;
      }
    },
  },

  mounted() {
    document.addEventListener('click', this.closeMenuOnOutsideClick);
  },

  beforeUnmount() {
    // Remove event listener when component is about to unmount
    document.removeEventListener('click', this.closeMenuOnOutsideClick);
  },

  async syncTaskToTrello(task) {
    try {
      const response = await fetch('/api/trello/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(task),
      });
      if (!response.ok) throw new Error('Failed to sync task to Trello');
      console.log('Task synced to Trello:', await response.json());
    } catch (error) {
      console.error('Error syncing task to Trello:', error);
    }
  },
  created() {
    if (this.isAuthenticated) {
      this.fetchTasks();
    }
  }
};
</script>



<style>

body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f4f4;
}

.welcome-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  text-align: center;
  box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.2);
}

.welcome-screen h1 {
  font-size: 3em;
  font-weight: bold;
  margin-bottom: 20px;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.welcome-screen p {
  font-size: 1.3em;
  margin: 15px 0;
  max-width: 600px;
  line-height: 1.6;
  padding: 10px;
}

.welcome-btn {
  padding: 15px 30px;
  font-size: 1.5em;
  font-weight: bold;
  color: white;
  background: linear-gradient(135deg, #ff512f, #dd2476);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease-in-out;
}

.welcome-btn:hover {
  background: linear-gradient(135deg, #ff8177, #dd5176);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
  transform: scale(1.05);
}
.menu-btn {
  position: absolute;
  padding: 17px;
  background-color: transparent;
  border: none;
  font-size: 30px;
  cursor: pointer;
  right: 10px;
}

.main-container {
  display: flex;
  position: relative;
}

.menu-options {
  position: absolute;
  top: 55px;
  right: 25px;
  background-color: #fff;
  border-radius: 7px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 10px;
  z-index: 10;
}

.logout-btn {
  background: linear-gradient(45deg, #c82333, #8e1f29);
}

.sync-btn {
  background: linear-gradient(45deg, #218838, #1d6d31);
}

.logout-btn,
.sync-btn {
  display: block;
  width: 100%;
  padding: 10px;
  color: white;
  border: none;
  margin: 5px 0;
  border-radius: 7px;
  cursor: pointer;
}

.logout-btn:hover {
  background: linear-gradient(45deg, #8e1f29, #a41d34);
}

.sync-btn:hover {
  background: linear-gradient(45deg, #1d6d31, #2a7f3b);
}


.add-task-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background: linear-gradient(135deg, #6a11cb, #2575fc);  color: white;
  border: none;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.add-task-btn:hover {
  transform: translateY(-5px); /* Легкий підйом кнопки */
  background: linear-gradient(135deg, #2575fc, #6a11cb); /* Зміна градієнта */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Підсилюємо тінь */
}

.add-task-btn:active {
  transform: translateY(1px); /* Кнопка "опускається" при натисканні */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Легша тінь при натисканні */
}

/* Активний стан кнопки */
.add-task-btn.active {
  background: linear-gradient(135deg, #2575fc, #6a11cb);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

</style>