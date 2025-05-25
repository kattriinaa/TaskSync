<template>
  <div class="login-container">
    <h1>Log In</h1>
    <form @submit.prevent="loginHandler">
      <input type="text" v-model="credentials.username" placeholder="Username" required />
      <input type="password" v-model="credentials.password" placeholder="Password" required />

      <p v-if="error" class="error-message">{{ error }}</p>

      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  props: {
    onLogin: {
      type: Function,
      required: false, // опціонально
    },
  },
  data() {
    return {
      credentials: { username: '', password: '' },
      error: '', // повідомлення про помилку
    };
  },
  methods: {
    loginHandler() {
      const validUsername = 'kattrina';
      const validPassword = 'tasksync';

      if (
        this.credentials.username === validUsername &&
        this.credentials.password === validPassword
      ) {
        this.error = '';
        if (this.onLogin) this.onLogin(this.credentials);
        // можеш також використати router.push або emit
      } else {
        this.error = '❌ Invalid username or password';
        // автоматичне очищення повідомлення через 3 секунди
        setTimeout(() => {
          this.error = '';
        }, 3000);
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  transition: all 0.3s ease-in-out;
}

.login-container h1 {
  font-family: 'Roboto', sans-serif;
  font-size: 28px;
  color: #009688;
  margin-bottom: 30px;
  text-align: center;
}

.login-container input[type="text"],
.login-container input[type="password"] {
  width: 100%;
  padding: 14px;
  margin-bottom: 20px;
  border: 1.5px solid #009688;
  border-radius: 6px;
  font-size: 16px;
  background-color: #f9f9f9;
  color: #333;
  box-sizing: border-box;
  transition: border 0.3s ease, background-color 0.3s ease;
}

.login-container input[type="text"]:focus,
.login-container input[type="password"]:focus {
  border: 2px solid #43a047;
  box-shadow: 0 0 5px #43a047;
}

.login-container button[type="submit"] {
  width: 100%;
  padding: 12px 0;
  font-size: 1.1em;
  font-weight: 600;
  background-color: #009688;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.login-container button[type="submit"]:hover {
  background-color: #43a047;
  color: #fff;
}

.login-container button:active {
  background-color: #00695c;
  transform: translateY(0);
}

.error-message {
  color: red;
  font-weight: 500;
  margin-bottom: 25px;
  font-family: 'Roboto', sans-serif;
  text-align: center;
}
</style>
