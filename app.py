from flask import Flask, jsonify, request, send_from_directory
from pymongo import MongoClient

app = Flask(__name__)

# Підключення до MongoDB Atlas
client = MongoClient("mongodb+srv://kushnirk548:LoXAxKWRK7REl0k8@tasksync.cbm4r.mongodb.net/<database>?retryWrites=true&w=majority")
db = client["task_sync"]  # Назва бази даних
tasks_collection = db["tasks"]  # Колекція для зберігання задач

# Функція для перетворення MongoDB документів у формат JSON
def serialize_task(task):
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "due_date": task["due_date"],
        "priority": task["priority"]
    }

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # Отримуємо всі задачі з колекції MongoDB
    tasks = tasks_collection.find()
    # Повертаємо їх у вигляді списку JSON
    return jsonify([serialize_task(task) for task in tasks])


@app.route('/api/tasks', methods=['POST'])
def add_task():
    task = request.json  # Отримуємо дані задачі з запиту
    task_id = tasks_collection.insert_one(task).inserted_id  # Зберігаємо задачу в MongoDB
    return jsonify({"id": str(task_id)}), 201  # Повертаємо ID створеної задачі


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
