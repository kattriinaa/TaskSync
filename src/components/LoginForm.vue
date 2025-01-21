<template>
  <div class="login-container">
    <h1>TaskSync</h1>
    <form @submit.prevent="loginHandler">
      <input type="text" v-model="credentials.username" placeholder="Username" required />
      <input type="password" v-model="credentials.password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  props: {
    onLogin: {
      type: Function,
      required: true,
    },
  },
  data() {
    return {
      credentials: { username: '', password: '' },
    };
  },
  methods: {
    loginHandler() {
      this.onLogin(this.credentials); // Викликаємо переданий метод
    },
  },
};
</script>

<style scoped>
.login-container {
  position: fixed; /* Встановлює фіксоване позиціонування для центрування */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* Переміщує вікно на половину своєї ширини та висоти */
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  width: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000; /* Зробить вікно поверх інших елементів */
}

.login-container h1 {
  margin-bottom: 20px;
  text-align: center;
}

.login-container input {
  width: 100%;
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.login-container button {
  width: 100%;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
}

.login-container button:hover {
  background-color: #0056b3;
}

</style>
