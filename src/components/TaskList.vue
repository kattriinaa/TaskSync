<template>
  <div class="task-list">
    <div
      v-for="task in tasks"
      :key="task.id"
      class="task-card"
      :class="{ completed: task.completed, important: task.priority === 'High' }"
      @click="$emit('openTask', task)"
    >
      <h3>{{ task.title }}</h3>
      <p>{{ task.description }}</p>
      <small>Дата: {{ task.due_date }}</small>

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
};
</script>

<style>
.task-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
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
</style>
