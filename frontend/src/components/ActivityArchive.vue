<template>
  <div class="activity-archive">
    <button class="back-btn" @click="$emit('back')">
        <span class="arrow">←</span>Back
    </button>
    <h2>Activity Archive</h2>
    <ul>
      <template v-for="(activity, idx) in activities" :key="idx">
        <li>
          <span class="type">{{ activity.type }}</span>
          <span class="title">{{ activity.taskTitle }}</span>
          <span class="ago">{{ timeAgo(activity.timestamp) }}</span>
          <div v-if="activity.type === 'edited' && activity.changes && Object.keys(activity.changes).length" class="activity-details">
            <div v-for="(change, field) in activity.changes" :key="field">
              <span class="field">{{ field }}:</span>
              <span class="was">was '{{ change.from }}'</span>
              <span class="arrow">→</span>
              <span class="became">became '{{ change.to }}'</span>
            </div>
          </div>
          <div v-else-if="activity.type === 'completed' && activity.details" class="activity-details">
            <div>
              <span class="field">Completed at:</span>
              <span class="to">{{ activity.details.completed_at ? new Date(activity.details.completed_at).toLocaleString() : 'now' }}</span>
            </div>
          </div>
        </li>
        <hr class="activity-separator" />
      </template>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'ActivityArchive',
  props: {
    activities: {
      type: Array,
      required: true
    }
  },
  methods: {
    timeAgo(date) {
      const now = new Date();
      const then = new Date(date);
      const seconds = Math.floor((now - then) / 1000);
      if (seconds < 60) return `${seconds} seconds ago`;
      const minutes = Math.floor(seconds / 60);
      if (minutes < 60) return `${minutes} minutes ago`;
      const hours = Math.floor(minutes / 60);
      if (hours < 24) return `${hours} hours ago`;
      const days = Math.floor(hours / 24);
      return `${days} days ago`;
    }
  }
}
</script>

<style scoped>
.activity-archive {
  color: #222;
  padding: 24px 32px;
}
.back-btn {
  background: linear-gradient(135deg, #009688,rgb(56, 112, 59));
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 18px;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(30,40,90,0.08);
  display: flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 10px;
  transition: background 0.2s, color 0.2s;
  margin-left: 0px;
}
.back-btn .arrow {
  font-size: 1em;
  font-weight: bold;
  margin-right: 3px;
  display: flex;
  align-items: center;
  color:rgb(255, 255, 255);
}
.back-btn:hover {
  background: linear-gradient(135deg, #43a047, #009688);
  color: #fff;
  box-shadow: 0 4px 16px rgba(30,40,90,0.16);
}
.dark-mode .back-btn {
  background: linear-gradient(135deg, #009688,rgb(56, 112, 59));
  color: #fff;
}
.dark-mode .back-btn:hover {
  background: linear-gradient(135deg, #43a047, #009688);
}
.activity-archive h2 {
  text-align: center;
  margin: 0 auto 24px auto;
  font-size: 3em;
  font-weight: bold;
}
ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
li {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 8px;
  font-size: 1em;
}
.type {
  font-weight: bold;
  color: #43a047;
}
.title {
  color:rgb(1, 49, 7);
  font-style: italic;
  font-weight: bold;
}
.ago {
  color: #aaa;
  font-size: 0.95em;
}
.activity-details {
  margin-left: 16px;
  font-size: 1em;
  color: #388e3c;
  background: #f7f9fa;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  padding: 6px 12px;
  margin-bottom: 4px;
}
.field {
  font-weight: 600;
  color: #009688;
}
.was {
  color: #e57373;
  margin-left: 6px;
}
.became {
  color: #43a047;
  margin-left: 6px;
}
.arrow {
  color: #222;
  margin: 0 4px;
}
.dark-mode .activity-archive {
  color: #fff;
  background: none;
  border: none;
  box-shadow: none;
}
.dark-mode .activity-details {
  background: rgba(0, 150, 136, 0.10);
  color: #b2dfdb;
  border: none;
}
.dark-mode .title{
  color:rgb(201, 255, 192);
}
.dark-mode .field {
  color: #43a047;
}
.dark-mode .arrow {
  color: #fff;
}
.activity-separator {
  border: none;
  border-top: 1.5px solid #e0e0e0;
  margin: 10px 0 18px 0;
}
.dark-mode .activity-separator {
  border-top: 1.5px solid #2e3a40;
}
</style> 