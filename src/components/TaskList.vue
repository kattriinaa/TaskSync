<template>
  <div>
    <!-- Фільтрація завдань -->
    <div class="filters">
      <button @click="filterTasks('all')" :class="{'active': currentFilter === 'all'}">Всі</button>
      <button @click="filterTasks('completed')" :class="{'active': currentFilter === 'completed'}">Виконані</button>
      <button @click="filterTasks('important')" :class="{'active': currentFilter === 'important'}">Важливі</button>
    </div>

    <!-- Список завдань -->
    <div class="task-list">
      <div
        v-for="task in filteredTasks"
        :key="task.id"
        class="task-card"
        :class="{ completed: task.completed, important: task.priority === 'High' }"
        @click="$emit('openTask', task)"
      >
        <h3>{{ task.title }}</h3>
        <p>{{ task.description }}</p>
        <small>Дата: {{ task.due_date }}</small>

        <!-- Галочка для позначки виконаного завдання -->
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
export default {
  props: {
    tasks: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      currentFilter: 'all', // Стартовий фільтр "Всі"
    };
  },
  computed: {
    // Фільтрація завдань залежно від обраного фільтру
    filteredTasks() {
      switch (this.currentFilter) {
        case 'completed':
          return this.tasks.filter((task) => task.completed);
        case 'important':
          return this.tasks.filter((task) => task.priority === 'High');
        default:
          return this.tasks; // Повертає всі завдання, якщо фільтр "all"
      }
    },
  },
  methods: {
    // Змінити фільтр
    filterTasks(filter) {
      this.currentFilter = filter;
    },
    // Перемикання виконаного стану завдання
    toggleTaskCompletion(task) {
      task.completed = !task.completed;
    },
    // Оновлення статусу виконаного завдання на сервері
    async updateTaskCompletion(task) {
      try {
        // Наприклад, оновлюємо статус виконаного завдання на сервері
        await this.$emit('updateTaskCompletion', task); // Ви можете передати task на сервер для оновлення
        console.log("Завдання оновлено:", task);
      } catch (error) {
        console.error("Не вдалося оновити завдання:", error);
      }
    },
  },
};
</script>


<style scoped>
/* Додаємо стилі для фільтрів */
.filters {
  display: flex;
  justify-content: flex-start; /* Починаємо зліва */
  gap: 20px; /* Відстань між кнопками */
  padding: 17px;
  margin-left: 11px;
}

.filters button {
  padding: 13px 25px;
  background: linear-gradient(135deg, #6a11cb, #2575fc); /* Градієнтний фон кнопок */
  color: white;
  border: none; /* Прибираємо рамки */
  border-radius: 30px; /* Закруглені краї кнопок */
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s, background 0.3s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.filters button:hover {
  transform: translateY(-5px); /* Легкий підйом кнопки */
  background: linear-gradient(135deg, #2575fc, #6a11cb); /* Зміна градієнта */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Підсилюємо тінь */
}

.filters button:active {
  transform: translateY(1px); /* Кнопка "опускається" при натисканні */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Легша тінь при натисканні */
}

/* Активний стан кнопок */
.filters button.active {
  background: linear-gradient(135deg, #2575fc, #6a11cb);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

/* Стилі для завдань */
.task-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: flex-start; /* Починаємо зліва */
  padding: 10px;
  margin-left: 17px;
}

/* Сучасна картка завдання */
.task-card {
  position: relative; /* Для позиціонування внутрішніх елементів */
  width: 300px;
  padding: 20px;
  background: linear-gradient(145deg, #ffffff, #f1f1f1); /* Сучасний світлий фон */
  border-radius: 13px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1), inset 0 1px 3px rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

/* Ефект при наведенні */
.task-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15), inset 0 1px 3px rgba(255, 255, 255, 0.5);
}

/* Завершене завдання */
.task-card.completed {
  background: linear-gradient(145deg, #dff8e1, #cce6d7); /* Світло-зелений градієнт */
}

/* Важливе завдання */
.task-card.important {
  border: 2px solid #ffc107; /* Яскрава рамка */
  box-shadow: 0 4px 12px rgba(255, 193, 7, 0.3); /* Жовта тінь */
}

/* Сучасний стиль для галочки */
.checkbox-container {
  position: absolute;
  bottom: 10px; /* Вирівнювання по нижньому краю */
  right: 10px; /* Вирівнювання по правому краю */
  cursor: pointer; /* Додаємо курсор для взаємодії */
  visibility: hidden; /* Спочатку приховано */
}

.task-card:hover .checkbox-container {
  visibility: visible; /* Показуємо галочку при наведенні на картку */
}

.checkbox-container input[type="checkbox"] {
  width: 24px; /* Більший розмір галочки */
  height: 24px;
  border-radius: 50%; /* Робимо галочку круглою */
  appearance: none; /* Відключаємо стандартне оформлення */
  border: 2px solid #007bff; /* Додаємо обводку */
  background-color: white; /* Білий фон */
  cursor: pointer;
  transition: all 0.3s ease;
}

/* Вибрана галочка */
.checkbox-container input[type="checkbox"]:checked {
  background: linear-gradient(135deg, #007bff, #2575fc); /* Градієнтна заливка */
  border-color: #2575fc; /* Колір обводки */
}

.checkbox-container input[type="checkbox"]:checked::before {
  content: '✔'; /* Додаємо галочку */
  position: absolute;
  top: 3px;
  left: 6px;
  font-size: 14px;
  color: white;
}
</style>
