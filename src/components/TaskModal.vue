<template>
  <div class="modal">
    <div class="modal-content">
      <h2>{{ mode === 'add' ? 'Нова задача' : 'Редагувати задачу' }}</h2>
      <form @submit.prevent="submitForm">
        <input type="text" v-model="localTask.title" placeholder="Заголовок" required />
        <textarea v-model="localTask.description" placeholder="Опис"></textarea>
        <input type="date" v-model="localTask.due_date" required />
        <select v-model="localTask.priority">
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
             
        <div class="modal-buttons">
          <button type="submit">Зберегти</button>
          <button type="button" @click="$emit('close')">Закрити</button>
          <!-- Кнопка "Видалити" -->
          <button
            v-if="mode === 'edit'"
            type="button"
            @click="$emit('delete', task)"
            class="delete-btn"
          >
            Видалити
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: ['task', 'mode'],
  data() {
    return {
      localTask: { ...this.task }
    };
  },
  methods: {
    submitForm() {
      this.$emit('save', this.localTask);
    }
  }
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
  background-color: white;
  padding: 30px;
  border-radius: 12px;
  width: 500px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  text-align: center;
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
  gap: 10px; /* Відстань між кнопками */
  justify-content: center;
}

.modal-content button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
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
}

.modal-content button[type="button"]:hover {
  background-color: #c82333;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
}

.delete-btn:hover {
  background-color: #c82333;
}
</style>
