
# TaskSync

TaskSync — це додаток для управління завданнями з можливістю синхронізації з Trello.  
Проєкт містить фронтенд на Vue.js та бекенд на Flask із використанням MongoDB.

## Структура проєкту

```
TaskSync/
├── backend/
│   ├── app.py
│   ├── .env
│   ├── venv/
│   └── __pycache__/
│
├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── SideMenu.vue
│   │   │   ├── TaskList.vue
│   │   │   ├── TaskModal.vue
│   │   │   ├── ActivityArchive.vue
│   │   │   ├── LoginForm.vue
│   │   │   └── UserProfile.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── babel.config.js
│   ├── jsconfig.json
│   ├── package.json
│   ├── package-lock.json
│   └── vue.config.js
│
├── .gitignore
└── README.md
```

---

## Необхідні умови

Перед початком роботи переконайтеся, що у вас встановлено:  
- Node.js (версія 14 або вище)  
- Python (версія 3.8 або вище)  
- MongoDB (локально або хмарний сервер, наприклад MongoDB Atlas)  
- Git  

---

## Інструкції зі встановлення

### 1. Клонування репозиторію
```bash
git clone https://github.com/kattriinaa/TaskSync.git
cd TaskSync
```

### 2. Налаштування бекенду

1. Перейдіть у папку бекенду і створіть віртуальне середовище:
```bash
cd backend
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

2. Встановіть залежності:
```bash
pip install flask flask-cors pymongo python-dotenv requests
```

3. Створіть файл `.env` у папці `backend` з такими змінними:
```
MONGO_URI=ваш_рядок_підключення_до_MongoDB
TRELLO_API_KEY=ваш_ключ_Trello
TRELLO_TOKEN=ваш_токен_Trello
TRELLO_BOARD_ID=""
TRELLO_LIST_ID=""
DONE_LIST_ID=""
```

> **ВАЖЛИВО:** `MONGO_URI` має містити актуальний рядок підключення до вашої бази даних.

---

### 3. Налаштування фронтенду

1. Перейдіть у папку фронтенду:
```bash
cd ../frontend
```

2. Встановіть Node.js залежності:
```bash
npm install
```

3. Переконайтесь, що у файлі `vue.config.js` налаштовано проксі для API (для уникнення проблем з CORS). Цей файл уже має бути у проєкті.

---

### 4. Запуск проєкту

- Запуск бекенду:
```bash
cd ../backend
# Активуйте віртуальне оточення, якщо ще не активоване
python app.py
```
Бекенд буде доступний за адресою: [http://localhost:5000](http://localhost:5000)

- Запуск фронтенду:
```bash
cd ../frontend
npm run serve
```
Фронтенд буде доступний за адресою: [http://localhost:8080](http://localhost:8080)

---

## Налаштування MongoDB Atlas

Якщо ви використовуєте MongoDB Atlas (хмарний сервіс), дотримуйтесь інструкцій:

1. Створіть акаунт на [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas).

2. Створіть безкоштовний кластер.

3. Додайте користувача бази даних з правами `readWrite`.

4. Додайте IP-адресу у "Network Access" (наприклад, вашу поточну IP або `0.0.0.0/0` для розробки).

5. Отримайте рядок підключення і вставте його у `.env` у змінну `MONGO_URI`.

---

## Особливості

- Створення, читання, редагування та видалення завдань  
- Синхронізація з Trello  
- Встановлення пріоритетів та термінів виконання  
- Позначення завдань як виконаних  
- Нагадування про завдання  

---

## Вирішення проблем

- Проблеми з CORS — перевірте проксі у `vue.config.js`.  
- Проблеми з MongoDB — перевірте `MONGO_URI` і чи запущений сервер бази.  
- Проблеми з Trello — перевірте ключі та токени у `.env`.  
