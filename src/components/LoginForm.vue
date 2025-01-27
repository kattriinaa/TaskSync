<template>
  <div class="login-container">
    <h1>Log In</h1>
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
/* Основні стилі для контейнера */
.login-container {
  position: fixed; /* Встановлює фіксоване позиціонування для центрування */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* Переміщує вікно на половину своєї ширини та висоти */
  background-color: #fff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000; /* Зробить вікно поверх інших елементів */
  transition: all 0.3s ease-in-out;
}

/* Стилі для заголовка */
.login-container h1 {
  font-family: 'Roboto', sans-serif;
  font-size: 28px;
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

/* Стилі для інпутів */
.login-container input {
  width: 100%;
  padding: 14px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  background-color: #f9f9f9;
  color: #333;
  box-sizing: border-box; /* Забезпечує рівномірне відступлення */
  transition: border 0.3s ease, background-color 0.3s ease;
}

/* Плавна зміна кольору межі та фону при фокусуванні */
.login-container input:focus {
  border-color: #007bff;
  background-color: #e7f3ff;
  outline: none;
}

/* Стилі для кнопки */
.login-container button {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  box-sizing: border-box; /* Забезпечує рівномірне відступлення */
}

/* Ефект при наведенні на кнопку */
.login-container button:hover {
  background-color: #0056b3;
  transform: translateY(-2px); /* Легке підняття кнопки */
}

/* Ефект при натисканні на кнопку */
.login-container button:active {
  background-color: #004085;
  transform: translateY(0); /* Відновлення положення */
}
</style>
