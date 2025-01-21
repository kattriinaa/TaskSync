from flask import Flask, jsonify, request, send_from_directory
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Підключення до MongoDB Atlas
client = MongoClient("mongodb+srv://kushnirk548:LoXAxKWRK7REl0k8@tasksync.cbm4r.mongodb.net/?retryWrites=true&w=majority")
db = client["task_sync"]  # Назва бази даних
tasks_collection = db["tasks"]  # Колекція для зберігання задач

# Функція для перетворення MongoDB документів у формат JSON
def serialize_task(task):
    return {
        "id": str(task["_id"]),  # Перетворення ObjectId у string
        "title": task["title"],
        "description": task["description"],
        "due_date": task["due_date"],
        "priority": task["priority"],
        "completed": task.get("completed", False)  # Додаємо поле "completed" за замовчуванням
    }

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # Отримуємо всі задачі з MongoDB
    tasks = tasks_collection.find()
    return jsonify([serialize_task(task) for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    # Отримуємо дані задачі з запиту
    task = request.json
    if not all(k in task for k in ("title", "description", "due_date", "priority")):
        return jsonify({"error": "Invalid task data"}), 400

    # Додаємо задачу до MongoDB
    task["completed"] = False  # Нові задачі не виконані за замовчуванням
    result = tasks_collection.insert_one(task)
    return jsonify({"id": str(result.inserted_id)}), 201

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Видаляємо задачу з MongoDB за її ID
    result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted successfully"}), 200

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    # Оновлюємо задачу за її ID
    task = request.json
    update_data = {k: v for k, v in task.items() if k in ("title", "description", "due_date", "priority", "completed")}
    result = tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})
    if result.matched_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

