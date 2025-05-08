<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode, 'light-mode': !isDarkMode }" :key="themeKey">
    <!-- Toast notifications -->
    <div class="toast-container">
      <div v-for="(toast, i) in toasts" :key="i" class="toast">{{ toast }}</div>
    </div>
    <!-- Login Form -->
    <LoginForm v-if="!isAuthenticated" @login="handleLogin"></LoginForm>

    <!-- Main Content -->
    <div v-else>
      <!-- Welcome Screen -->
      <div v-if="!hasVisited" class="welcome-screen">
        <h1>Welcome to TaskSync!</h1>
        <p>TaskSync is your perfect planner for organizing tasks and syncing with Trello.</p>
        <button class="welcome-btn" @click="closeWelcome">Go to Planner</button>
      </div>

      <!-- Main Content -->
      <div v-else class="main-layout">
        <!-- Side Menu -->
        <SideMenu
          v-if="currentView !== 'profile' && currentView !== 'archive'"
          :tasks="tasks"
          :currentFilter="currentFilter"
          :currentView="currentView"
          @filter-change="handleFilterChange"
          @theme-changed="toggleTheme"
          @navigate="handleNavigation"
          @sync-trello="fetchTrelloTasks"
          @logout="logout"
        />

        <!-- Main Content Area -->
        <div class="content-area">
          <!-- User Profile -->
          <UserProfile
            v-if="currentView === 'profile'"
            :tasks="tasks"
            :isDarkMode="isDarkMode"
            @back="handleNavigation('tasks')"
            @profile-updated="handleProfileUpdate"
            @theme-changed="toggleTheme"
            @logout="logout"
          />

          <!-- Activity Archive -->
          <ActivityArchive
            v-else-if="currentView === 'archive'"
            :activities="activities"
            @back="handleNavigation('tasks')"
          />

          <!-- Tasks View -->
          <div v-else class="task-content">
            <TaskList
              :tasks="filteredTasks"
              :filterCriteria="filterCriteria"
              @openTask="openTask"
              @showAddModal="showAddTaskModal"
              @close="closeModal"
              @completed="handleTaskCompleted"
            />
            <TaskModal
              v-if="showModal"
              :task="currentTask || { title: '', description: '', due_date: '', priority: '', syncToTrello: false }"
              :mode="modalMode"
              @save="saveTask"
              @request-delete="deleteTask"
              @close="closeModal"
              @success="showSuccess"
              @error="showError"
            />
          </div>

          <!-- Add Task Button - Only show in tasks view -->
          <button
            v-if="currentView === 'tasks'"
            class="add-task-btn"
            @click="showAddTaskModal"
            :disabled="showModal"
          >+</button>

          <!-- Archive Floating Button -->
          <button
            v-if="currentView === 'tasks'"
            class="archive-fab-btn"
            @click="handleNavigation('archive')"
            :disabled="showModal"
            title="Archive"
          >
            <span style="font-size:1em;">Archive</span>
          </button>
        </div>
      </div>
    </div>
    <transition name="fade">
      <div v-if="showSuccessModal" class="global-modal success-modal">
        <div class="modal-content">{{ successMessage }}</div>
      </div>
    </transition>
    <transition name="fade">
      <div v-if="showConfirmModal" class="global-modal confirm-modal">
        <div class="modal-content">
          <div>{{ confirmMessage }}</div>
          <div class="modal-buttons">
            <button @click="confirmYes">Yes</button>
            <button @click="confirmNo">No</button>
          </div>
        </div>
      </div>
    </transition>
    <transition name="fade">
      <div v-if="showErrorModal" class="global-modal error-modal">
        <div class="modal-content">{{ errorMessage }}</div>
      </div>
    </transition>
  </div>
</template>

<script>
import LoginForm from './components/LoginForm.vue';
import TaskList from './components/TaskList.vue';
import TaskModal from './components/TaskModal.vue';
import SideMenu from './components/SideMenu.vue';
import UserProfile from './components/UserProfile.vue';
import ActivityArchive from './components/ActivityArchive.vue';

export default {
  components: {
    LoginForm,
    TaskList,
    TaskModal,
    SideMenu,
    UserProfile,
    ActivityArchive
  },
  data() {
    return {
      isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
      hasVisited: localStorage.getItem('hasVisited') === 'true',
      tasks: [],
      filteredTasks: [],
      showModal: false,
      currentTask: null,
      modalMode: 'add',
      filterCriteria: {},
      currentFilter: 'all',
      currentView: 'tasks',
      isDarkMode: false, // default, will be set in created()
      notifiedReminders: [], // Track notified task IDs
      toasts: [], // Toast notifications
      themeKey: 0, // Used to force re-render on theme change
      activities: JSON.parse(localStorage.getItem('activities') || '[]'),
      showSuccessModal: false,
      successMessage: '',
      showConfirmModal: false,
      confirmCallback: null,
      confirmMessage: '',
      showErrorModal: false,
      errorMessage: '',
    };
  },
  watch: {
    isDarkMode(newVal) {
      if (newVal) {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
      } else {
        document.body.classList.remove('dark-mode');
        document.body.classList.add('light-mode');
      }
    }
  },
  methods: {
    handleLogin() {
      this.isAuthenticated = true;
      localStorage.setItem('isAuthenticated', 'true');
      this.fetchTasks();
      this.fetchTrelloTasks();
      this.hasVisited = false;
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

    async saveActivitiesToStorage() {
      localStorage.setItem('activities', JSON.stringify(this.activities));
    },

    async saveTask(task) {
      try {
        let response, newTask;
        const now = new Date();
        if (this.modalMode === 'add') {
          response = await fetch('/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(task),
          });
          if (!response.ok) throw new Error('Failed to add task');
          newTask = await response.json();
          this.tasks.push(newTask);
          this.activities.unshift({ type: 'added', taskTitle: newTask.title, timestamp: now, details: { ...newTask } });
          this.saveActivitiesToStorage();
          this.showSuccess('Task added!');
          if (task.syncToTrello) {
            await this.syncTaskToTrello(newTask);
            this.activities.unshift({ type: 'synchronized', taskTitle: newTask.title, timestamp: new Date() });
            this.saveActivitiesToStorage();
            this.showSuccess('Task synchronized!');
          }
        } else {
          // Find the old task for diff
          const oldTask = this.tasks.find(t => t.id === task.id);
          response = await fetch(`/api/tasks/${task.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(task),
          });
          if (!response.ok) throw new Error('Failed to update task');
          const updatedTask = await response.json();
          const index = this.tasks.findIndex(t => t.id === task.id);
          if (index !== -1) this.tasks.splice(index, 1, updatedTask);
          // Compute changed fields
          const changedFields = {};
          if (oldTask) {
            for (const key of Object.keys(task)) {
              if (task[key] !== oldTask[key]) {
                changedFields[key] = { from: oldTask[key], to: task[key] };
              }
            }
          }
          this.activities.unshift({ type: 'edited', taskTitle: task.title, timestamp: now, changes: changedFields });
          this.saveActivitiesToStorage();
          this.showSuccess('Task updated!');
        }
        this.applyCurrentFilters();
        this.showModal = false;
      } catch (error) {
        console.error('Error saving task:', error);
      }
    },

    async deleteTask(task) {
      this.askConfirm('Are you sure you want to delete this task?', async () => {
        try {
          await fetch(`/api/tasks/${task.id}`, { method: 'DELETE' });
          this.tasks = this.tasks.filter(t => t.id !== task.id);
          this.activities.unshift({ type: 'deleted', taskTitle: task.title, timestamp: new Date(), details: { ...task } });
          this.saveActivitiesToStorage();
          this.applyCurrentFilters();
          this.showModal = false;
          this.showSuccess('Task deleted!');
        } catch (error) {
          console.error('Error deleting task:', error);
        }
      });
    },

    // Old filter method, kept for backward compatibility
    filterTasks(filterType) {
      this.currentFilter = filterType;
      this.applyCurrentFilters();
    },

    // New method to handle filter changes from SideMenu
    handleFilterChange(filters) {
      this.filterCriteria = filters;
      this.applyCurrentFilters();
    },

    // Apply all active filters to tasks
    applyCurrentFilters() {
      // Start with all tasks
      let result = [...this.tasks];
      
      // Apply basic filter (all, important, completed)
      if (this.currentFilter === 'important') {
        result = result.filter(task => task.priority === 'High');
      } else if (this.currentFilter === 'completed') {
        result = result.filter(task => task.completed);
      }
      
      // Apply date filters if any
      if (this.filterCriteria) {
        // Filter by month
        if (this.filterCriteria.month) {
          result = result.filter(task => {
            if (!task.due_date) return false;
            return task.due_date.substring(5, 7) === this.filterCriteria.month;
          });
        }
        
        // Filter by specific date
        if (this.filterCriteria.date) {
          const filterDate = new Date(this.filterCriteria.date).toISOString().split('T')[0];
          result = result.filter(task => {
            if (!task.due_date) return false;
            return task.due_date.split('T')[0] === filterDate;
          });
        }
        
        // Filter by relative due date
        if (this.filterCriteria.dueDate) {
          const today = new Date();
          const tomorrow = new Date();
          tomorrow.setDate(today.getDate() + 1);
          const nextWeek = new Date();
          nextWeek.setDate(today.getDate() + 7);
          
          const todayStr = today.toISOString().split('T')[0];
          const tomorrowStr = tomorrow.toISOString().split('T')[0];
          
          if (this.filterCriteria.dueDate === 'today') {
            result = result.filter(task => {
              if (!task.due_date) return false;
              return task.due_date.split('T')[0] === todayStr;
            });
          } else if (this.filterCriteria.dueDate === 'tomorrow') {
            result = result.filter(task => {
              if (!task.due_date) return false;
              return task.due_date.split('T')[0] === tomorrowStr;
            });
          } else if (this.filterCriteria.dueDate === 'nextWeek') {
            result = result.filter(task => {
              if (!task.due_date) return false;
              const taskDate = new Date(task.due_date);
              return taskDate > today && taskDate <= nextWeek;
            });
          }
        }
      }
      
      this.filteredTasks = result;
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
        this.applyCurrentFilters();
      } catch (error) {
        console.error('Error syncing tasks from Trello:', error);
      }
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

    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem('darkMode', this.isDarkMode);
      if (this.isDarkMode) {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
      } else {
        document.body.classList.remove('dark-mode');
        document.body.classList.add('light-mode');
      }
      // Force re-render to fix style glitches
      this.themeKey++;
    },

    handleNavigation(view) {
      this.currentView = view;
      localStorage.setItem('currentView', view);
    },

    handleProfileUpdate(profileData) {
      // Update local storage and state if needed
      localStorage.setItem('username', profileData.username);
      localStorage.setItem('email', profileData.email);
      localStorage.setItem('userAvatar', profileData.avatar);
    },

    logout() {
      this.isAuthenticated = false;
      localStorage.removeItem('isAuthenticated');
      this.hasVisited = false;
      localStorage.removeItem('hasVisited');
    },

    checkReminders() {
      const now = new Date();
      const nowDateStr = now.toISOString().slice(0, 10); // 'YYYY-MM-DD'
      const nowHour = now.getHours(); // Normal logic
      this.tasks.forEach(task => {
        if (!task.due_date || task.reminderDaysBefore === null || task.reminderDaysBefore === undefined || task.completed) return;
        const dueDate = new Date(task.due_date);
        const dueDateStr = dueDate.toISOString().slice(0, 10);
        // Day before: show at 9:00 AM the day before
        if (
          task.reminderDaysBefore == 1 &&
          nowHour === 9 &&
          nowDateStr === new Date(dueDate.getTime() - 86400000).toISOString().slice(0, 10) &&
          !this.notifiedReminders.includes(task.id + '-1d')
        ) {
          this.showReminderNotification(task);
          this.notifiedReminders.push(task.id + '-1d');
        }
        // Same day: show at 9:00 AM on due date
        if (
          task.reminderDaysBefore == 0 &&
          nowHour === 9 &&
          nowDateStr === dueDateStr &&
          !this.notifiedReminders.includes(task.id + '-0d')
        ) {
          this.showReminderNotification(task);
          this.notifiedReminders.push(task.id + '-0d');
        }
      });
    },

    showToast(message) {
      this.toasts.push(message);
      setTimeout(() => {
        this.toasts.shift();
      }, 5000);
    },

    showReminderNotification(task) {
      const message = `Reminder: Task "${task.title}" is due on ${task.due_date}`;
      this.showToast(message);
      // Browser notification
      if (window.Notification && Notification.permission === 'granted') {
        new Notification('Task Reminder', { body: message });
      } else if (window.Notification && Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
          if (permission === 'granted') {
            new Notification('Task Reminder', { body: message });
          }
        });
      }
    },

    showSuccess(msg) {
      this.successMessage = msg;
      this.showSuccessModal = true;
      setTimeout(() => { this.showSuccessModal = false; }, 1500);
    },

    showError(msg) {
      this.errorMessage = msg;
      this.showErrorModal = true;
      setTimeout(() => { this.showErrorModal = false; }, 3000);
    },

    askConfirm(msg, callback) {
      this.confirmMessage = msg;
      this.confirmCallback = callback;
      this.showConfirmModal = true;
    },

    confirmYes() {
      if (this.confirmCallback) this.confirmCallback();
      this.showConfirmModal = false;
    },

    confirmNo() {
      this.showConfirmModal = false;
    },

    handleTaskCompleted(task) {
      this.activities.unshift({
        type: 'completed',
        taskTitle: task.title,
        timestamp: new Date(),
        details: { ...task }
      });
      this.saveActivitiesToStorage();
    },
  },
  created() {
    // Theme persistence: check localStorage and apply theme immediately
    const savedTheme = localStorage.getItem('darkMode');
    this.isDarkMode = savedTheme === 'true';
    if (this.isDarkMode) {
      document.body.classList.add('dark-mode');
      document.body.classList.remove('light-mode');
    } else {
      document.body.classList.remove('dark-mode');
      document.body.classList.add('light-mode');
    }
    if (this.isAuthenticated) {
      this.fetchTasks();
    }
    const savedView = localStorage.getItem('currentView');
    if (savedView === 'archive' || savedView === 'tasks' || savedView === 'profile') {
      this.currentView = savedView;
    } else {
      this.currentView = 'tasks';
    }
  },
  mounted() {
    // Start reminder interval
    setInterval(this.checkReminders, 60000);
    // Ask for notification permission on load
    if (window.Notification && Notification.permission !== 'granted') {
      Notification.requestPermission();
    }
  }
};
</script>

<style>
html, body, #app, .main-layout, .content-area, .task-board, .column {
  min-width: 0 !important;
  overflow-x: hidden !important;
  box-sizing: border-box !important;
}
body, #app, .main-layout, .content-area {
  padding: 0 !important;
  margin: 0 !important;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  transition: all 0.3s ease;
}

body.dark-mode {
  background-color: #121212;
  color: #ffffff;
}

#app {
  min-height: 100vh;
}

.main-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

.content-area {
  flex-grow: 1;
  position: relative;
  background-color: #ffffff;
  transition: all 0.3s ease;
  width: 100%;
}

.dark-mode .content-area {
  background-color: #1a1a1a;
  color: #ffffff;
}

.welcome-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg,rgb(13, 83, 76),rgb(28, 67, 30));
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
  background: linear-gradient(135deg, #009688, #00695c);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease-in-out;
}

.welcome-btn:hover {
  background: linear-gradient(135deg, #009688, #00695c);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
  transform: scale(1.05);
}

.add-task-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background: linear-gradient(135deg, #009688,rgb(56, 112, 59));
  color: white;
  border: none;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 1000;
}

.add-task-btn:hover {
  transform: translateY(-5px);
  background: linear-gradient(135deg, #43a047, #009688);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.add-task-btn:active {
  transform: translateY(1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dark-mode .add-task-btn {
  background: linear-gradient(135deg, #009688,rgb(56, 112, 59));
}

.dark-mode .add-task-btn:hover {
  background: linear-gradient(135deg, #43a047, #009688);
}

.toast-container {
  position: fixed;
  bottom: 32px;
  right: 32px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.toast {
  background: #009688;
  color: #fff;
  padding: 16px 28px;
  border-radius: 10px;
  font-size: 1.1em;
  box-shadow: 0 4px 16px rgba(0,0,0,0.18);
  min-width: 220px;
  max-width: 340px;
  animation: fadein 0.3s, fadeout 0.3s 4.7s;
}
@keyframes fadein {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeout {
  from { opacity: 1; }
  to { opacity: 0; }
}
.fade-enter-active, .fade-leave-active { transition: opacity 0.4s; }
.fade-enter, .fade-leave-to { opacity: 0; }
.global-modal {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.35);
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
}
.global-modal .modal-content {
  background: #23272f;
  color: #fff;
  border-radius: 12px;
  padding: 32px 40px;
  font-size: 1.2em;
  box-shadow: 0 8px 32px rgba(30,40,90,0.18);
  text-align: center;
  min-width: 220px;
}
.global-modal.success-modal .modal-content {
  background: #009688;
  color: #fff;
}
.global-modal.confirm-modal .modal-content {
  background: #23272f;
  color: #fff;
}
.global-modal .modal-buttons {
  margin-top: 18px;
  display: flex;
  gap: 18px;
  justify-content: center;
}
.global-modal .modal-buttons button {
  background: #009688;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 22px;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.global-modal .modal-buttons button:hover {
  background: #43a047;
}
.global-modal.error-modal .modal-content {
  background: #d32f2f;
  color: #fff;
}

.archive-fab-btn {
  position: fixed;
  top: 30px;
  right: 30px;
  background: linear-gradient(135deg, #009688,rgb(56, 112, 59));
  color: white;
  border: none;
  width: 100px;
  height: 35px;
  border-radius: 20px;
  font-size: 1.3em;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.archive-fab-btn:hover {
  background: linear-gradient(135deg, #43a047, #009688);
  transform: translateY(-5px);
}

.add-task-btn:disabled,
.archive-fab-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
  filter: grayscale(0.5);
}
</style>