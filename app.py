from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS, cross_origin
import requests
from dotenv import load_dotenv
import os

# Ініціалізація Flask застосунку
app = Flask(__name__)
CORS(app)  # Додаємо CORS для всіх ендпоінтів

# Завантаження змінних середовища
load_dotenv()

# MongoDB підключення
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["task_sync"]
tasks_collection = db["tasks"]

# Trello API ключі
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_LIST_ID = os.getenv("TRELLO_LIST_ID")


# Функція для перетворення MongoDB документів у JSON
def serialize_task(task):
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "due_date": task.get("due_date"),
        "priority": task["priority"],
        "completed": task.get("completed", False),
        "trello_task_id": task.get("trello_task_id"),
    }


# Ендпоінт для отримання завдань
@app.route('/api/tasks', methods=['GET'])
@cross_origin()  # Додаємо CORS для цього ендпоінта
def get_tasks():
    tasks = tasks_collection.find()
    return jsonify([serialize_task(task) for task in tasks]), 200


# Ендпоінт для додавання нового завдання
@app.route('/api/tasks', methods=['POST'])
@cross_origin()
def add_task():
    task = request.json
    app.logger.info(f"Received task data: {task}")
    if not task or not task.get("title"):
        app.logger.error("Invalid task data")
        return jsonify({"error": "Invalid task data"}), 400

    new_task = {
        "title": task["title"],
        "description": task.get("description", ""),
        "due_date": task.get("due_date"),
        "priority": task.get("priority", "Medium"),
        "completed": False,
    }
    app.logger.info(f"New task to process: {new_task}")

    existing_task = tasks_collection.find_one({"title": new_task["title"], "description": new_task["description"]})
    app.logger.info(f"Existing task: {existing_task}")
    if existing_task and "trello_task_id" in existing_task:
        return jsonify({"error": "Task already exists and is synced with Trello"}), 400

    trello_response = sync_task_to_trello(new_task)
    app.logger.info(f"Trello response: {trello_response}")
    if trello_response.get("error"):
        return jsonify(trello_response), 500

    new_task["trello_task_id"] = trello_response.get("id")

    try:
        result = tasks_collection.insert_one(new_task)
        new_task["_id"] = str(result.inserted_id)
        app.logger.info(f"Task successfully saved: {new_task}")
        return jsonify(serialize_task(new_task)), 201
    except Exception as e:
        app.logger.error(f"Error saving task to MongoDB: {str(e)}")
        return jsonify({"error": "Failed to save task to database"}), 500


@app.route('/api/tasks/<task_id>', methods=['PUT'])
@cross_origin()
def update_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    update_fields = {}
    
    if 'completed' in data:
        update_fields['completed'] = data['completed']
    
    if 'due_date' in data:
        update_fields['due_date'] = data['due_date']
    
    if 'priority' in data:
        update_fields['priority'] = data['priority']
    
    if 'description' in data:
        update_fields['description'] = data['description']
    
    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400
    
    result = tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_fields}
    )
    
    if result.matched_count == 0:
        return jsonify({"error": "Task not found"}), 404

    updated_task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    return jsonify(serialize_task(updated_task)), 200

# Ендпоінт для видалення завдання
@app.route('/api/tasks/<task_id>', methods=['DELETE'])
@cross_origin()  # Додаємо CORS для цього ендпоінта
def delete_task(task_id):
    if not ObjectId.is_valid(task_id):
        return jsonify({"error": "Invalid task ID"}), 400

    existing_task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not existing_task:
        return jsonify({"error": "Task not found"}), 404

    trello_id = existing_task.get("trello_task_id")
    if trello_id:
        delete_trello_task(trello_id)

    try:
        tasks_collection.delete_one({"_id": ObjectId(task_id)})
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error deleting task from MongoDB: {str(e)}")
        return jsonify({"error": "Failed to delete task"}), 500


@app.route('/sync-task', methods=['POST', 'OPTIONS'])
@cross_origin()  # Додаємо CORS для цього ендпоінта
def sync_task():
    if request.method == 'OPTIONS':
        # Обробка CORS
        response = jsonify({"message": "CORS preflight"})
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    # Логіка для синхронізації завдання
    task_data = request.json
    if not task_data or not task_data.get("title"):
        return jsonify({"error": "Invalid task data"}), 400

    # Синхронізація логіки (додайте ваш код тут)
    return jsonify({"message": "Task synced successfully!"}), 200


# Ендпоінт для отримання завдань із Trello та збереження їх у базі даних
@app.route('/api/trello/tasks/<list_id>', methods=['GET'])
@cross_origin()  # Додаємо CORS для цього ендпоінта
def get_trello_tasks(list_id):
    url = f"https://api.trello.com/1/lists/{list_id}/cards"
    params = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            trello_tasks = response.json()

            # Збереження завдань у MongoDB, якщо їх немає
            for task in trello_tasks:
                existing_task = tasks_collection.find_one({"trello_task_id": task["id"]})
                if not existing_task:
                    # Формуємо нове завдання для збереження в MongoDB
                    new_task = {
                        "title": task["name"],
                        "description": task.get("desc", ""),
                        "due_date": task.get("due", None),
                        "priority": "Medium",  # Встановіть пріоритет за необхідності
                        "completed": task["closed"],  # Встановлюємо статус завершення
                        "trello_task_id": task["id"]
                    }
                    # Збереження нового завдання
                    tasks_collection.insert_one(new_task)

            return jsonify(trello_tasks), 200
        else:
            return jsonify({"error": "Failed to fetch tasks from Trello"}), response.status_code
    except Exception as e:
        app.logger.error(f"Error fetching tasks from Trello: {str(e)}")
        return jsonify({"error": "Failed to fetch tasks from Trello"}), 500


# Допоміжна функція для синхронізації завдання з Trello
def sync_task_to_trello(task):
    url = "https://api.trello.com/1/cards"
    params = {
        "name": task["title"],
        "desc": task["description"],
        "due": task.get("due_date"),
        "idList": TRELLO_LIST_ID,
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    }
    try:
        response = requests.post(url, data=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to create task on Trello", "details": response.json()}
    except Exception as e:
        app.logger.error(f"Error syncing task with Trello: {str(e)}")
        return {"error": "Failed to sync task with Trello"}


# Допоміжна функція для оновлення завдання на Trello
def update_trello_task(trello_task_id, update_data):
    url = f"https://api.trello.com/1/cards/{trello_task_id}"
    params = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    }
    params.update(update_data)  # Додаємо оновлені дані
    try:
        response = requests.put(url, data=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to update task on Trello", "details": response.json()}
    except Exception as e:
        app.logger.error(f"Error updating task on Trello: {str(e)}")
        return {"error": "Failed to update task on Trello"}


# Допоміжна функція для видалення завдання з Trello
def delete_trello_task(trello_task_id):
    url = f"https://api.trello.com/1/cards/{trello_task_id}"
    params = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    }
    try:
        response = requests.delete(url, params=params)
        if response.status_code != 200:
            app.logger.error(f"Failed to delete task from Trello: {response.text}")
    except Exception as e:
        app.logger.error(f"Error deleting task from Trello: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)