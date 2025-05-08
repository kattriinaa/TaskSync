<template>
  <div class="modal">
    <div class="modal-content">
      <!-- Кнопка синхронізації в правому верхньому кутку модального вікна -->
      <button 
        v-if="mode === 'edit'" 
        class="sync-button-circle" 
        @click="syncTaskWithTrello(task.id)"
        aria-label="Sync with Trello"
      >
        <i class="fa fa-sync" aria-hidden="true"></i> <!-- Іконка синхронізації -->
      </button>

      <h2>{{ mode === 'add' ? 'New task' : 'Edit task' }}</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <input type="text" v-model="localTask.title" placeholder="Title" required />
          <span v-if="submitted && !localTask.title" class="error">Fill in this field</span>
        </div>

        <div class="form-group">
          <textarea v-model="localTask.description" placeholder="Description"></textarea>
        </div>

        <div class="form-group">
          <input type="date" v-model="localTask.due_date" required />
          <span v-if="submitted && !localTask.due_date" class="error">Fill in this field</span>
        </div>
        <!-- Reminder field -->
        <div class="form-group">
          <label for="reminder">Reminder:</label>
          <select id="reminder" v-model="localTask.reminderDaysBefore">
            <option :value="null">No Reminder</option>
            <option :value="0">On the same day</option>
            <option :value="1">The day before</option>
          </select>
        </div>

        <div class="form-group">
          <select v-model="localTask.priority" required>
            <option value="" disabled>Select priority</option>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
          <span v-if="submitted && !localTask.priority" class="error">Select priority</span>
        </div>

        <div class="form-group" v-if="mode === 'add'">
          <label>
            <input type="checkbox" v-model="localTask.syncToTrello" /> Synchronize with Trello
          </label>
        </div>

        <div class="modal-buttons">
          <button type="submit">Save</button>
          <button type="button" @click="$emit('close')">Close</button>
          <button 
            v-if="mode === 'edit'" 
            type="button" 
            @click="confirmDelete"
          >
            Delete
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    task: {
      type: Object,
      default: () => ({
        title: '',
        description: '',
        due_date: '',
        priority: '',
        syncToTrello: false,
        completed: false, // Додаємо статус виконаного
        reminderDaysBefore: null, // New: reminder (0 = same day, 1 = day before)
      }),
    },
    mode: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      localTask: { ...this.task },
      submitted: false,
    };
  },
  methods: {
    submitForm() {
      this.submitted = true;

      if (!this.localTask.title || !this.localTask.due_date || !this.localTask.priority) {
        console.warn("Не всі поля заповнені.");
        return;
      }

      // Перевірка, чи потрібно синхронізувати завдання з Trello
      if (this.localTask.syncToTrello) {
        this.syncTaskToBackend(this.localTask); // Викликаємо бекенд для синхронізації з Trello
      }

      // Еміт події save з даними:
      console.log("Еміт події save з даними:", this.localTask);
      this.$emit("save", this.localTask);
      this.$emit("close");
    },

    confirmDelete() {
      this.$emit('request-delete', this.localTask);
    },

    async syncTaskToBackend(task) {
  try {
    await axios.post('http://localhost:5000/sync-task', task);
        this.$emit("success", 'Task synchronized with Trello!');
        this.$emit("close");
    await this.getUpdatedTasks();
    this.$emit("syncCompleted");
  } catch (error) {
    if (error.response && error.response.status === 400 && error.response.data.error) {
          this.$emit("error", error.response.data.error + " Please change the task title.");
    } else {
          console.error('Failed to sync task:', error);
          this.$emit("error", 'Failed to sync task with Trello.');
    }
  }
},

async syncTaskWithTrello(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}/sync`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const data = await response.json();
        if (response.ok) {
          this.$emit("success", data.message);
        } else {
          this.$emit("error", data.error);
        }
    } catch (error) {
        console.error("Error syncing task with Trello:", error);
        this.$emit("error", "Failed to sync task with Trello.");
    }
}, 

    // Метод для отримання оновлених завдань після синхронізації
    async getUpdatedTasks() {
      try {
        // Отримуємо всі завдання з бекенду
        const response = await axios.get('http://localhost:5000/api/tasks');
        
        // Оновлюємо список завдань
        this.$emit('update-tasks', response.data); // Еміт для оновлення завдань у батьківському компоненті
      } catch (error) {
        console.error('Не вдалося отримати оновлені завдання:', error);
      }
    },
    

    markAsCompleted() {
      this.localTask.completed = true; // Встановлюємо статус виконаного завдання
      console.log("Завдання виконано:", this.localTask); // Лог для перевірки
      this.$emit("save", this.localTask); // Емітимо збереження зміненого завдання
    },
  },
};
</script>

<style>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  position: relative; /* важливо для правильного позиціонування кнопки */
  background-color: white;
  padding: 30px;
  border-radius: 12px;
  width: 500px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.sync-button-circle {
  position: absolute;
  top: 15px; /* Відступ з верхнього краю */
  right: 15px; /* Відступ з правого краю */
  color: black;
  font-size: 24px;
  width: 40px;  /* Ширина кнопки */
  height: 40px; /* Висота кнопки, яка має бути рівною ширині для ідеальної круглої форми */
  border-radius: 50%; /* Кругла форма */
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 10; /* Завжди на передньому плані */
}

.sync-button-circle:hover {
  background: linear-gradient(135deg,rgb(154, 154, 154),rgb(101, 103, 105));
}

.sync-button-circle i {
  font-size: 18px; /* Розмір іконки */
}

.modal-content input,
.modal-content textarea,
.modal-content select {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.modal-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.modal-content button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.modal-content button[type='submit'] {
  background: linear-gradient(135deg, #007bff, #06294f);
  color: white;
  border: none;
}

.modal-content button[type='submit']:hover {
  background: linear-gradient(135deg, #0056b3, #06294f);
}

.modal-content button[type='button'] {
  background: linear-gradient(135deg, #dc3545, #90131f);
  color: white;
  border: none;
}

.modal-content button[type='button']:hover {
  background: linear-gradient(135deg, #c82333, #90131f);
}

.error {
  color: red;
  font-size: 12px;
  margin-top: -10px;
  margin-bottom: 10px;
  display: block;
}

.form-group {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 17px;
  margin: 15px;
}

.form-group input[type="checkbox"] {
  width: 17px;
  height: 17px;
  border-radius: 4px;
  border: 2px solid #007bff;
  background-color: white;
  cursor: pointer;
}

/* --- DARK MODE STYLES --- */
.dark-mode .modal-content {
  background-color: #232323;
  color: #f5f5f5;
  box-shadow: 0 4px 18px rgba(0,0,0,0.5);
}
.dark-mode .modal-content input,
.dark-mode .modal-content textarea,
.dark-mode .modal-content select {
  background: #181818;
  color: #fff;
  border: 1px solid #444;
}
.dark-mode .modal-content input:focus,
.dark-mode .modal-content textarea:focus,
.dark-mode .modal-content select:focus {
  border: 1.5px solid #3887fa;
}
.dark-mode .modal-content button[type='submit'] {
  background: linear-gradient(135deg, #1976d2, #1565c0);
  color: #fff;
}
.dark-mode .modal-content button[type='submit']:hover {
  background: linear-gradient(135deg, #3887fa, #1976d2);
}
.dark-mode .modal-content button[type='button'] {
  background: linear-gradient(135deg, #b71c1c, #90131f);
  color: #fff;
}
.dark-mode .modal-content button[type='button']:hover {
  background: linear-gradient(135deg, #ef5350, #b71c1c);
}
.dark-mode .sync-button-circle {
  background: linear-gradient(135deg, #1976d2, #1565c0);
  color: #fff;
}
.dark-mode .sync-button-circle:hover {
  background: linear-gradient(135deg, #3887fa, #1976d2);
}
.dark-mode .form-group input[type="checkbox"] {
  background: #232323;
  border: 2px solid #3887fa;
}
</style>
