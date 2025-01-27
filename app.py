from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

# Завантаження змінних середовища з файлу .env
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
    }


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = tasks_collection.find()
    return jsonify([serialize_task(task) for task in tasks]), 200


@app.route('/api/tasks', methods=['POST'])
def add_task():
    task = request.json
    if not task or not task.get("title"):
        return jsonify({"error": "Invalid task data"}), 400

    new_task = {
        "title": task["title"],
        "description": task.get("description", ""),
        "due_date": task.get("due_date"),
        "priority": task.get("priority", "Medium"),
        "completed": False,
    }

    # Синхронізація з Trello
    trello_response = sync_task_to_trello(new_task)
    if trello_response.get("error"):
        return jsonify(trello_response), 500

    new_task["trello_task_id"] = trello_response.get("id")

    # Збереження в базі даних
    result = tasks_collection.insert_one(new_task)
    new_task["_id"] = result.inserted_id
    return jsonify(serialize_task(new_task)), 201


@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    if not ObjectId.is_valid(task_id):
        return jsonify({"error": "Invalid task ID"}), 400

    task_data = request.json
    update_data = {k: v for k, v in task_data.items() if k in ["title", "description", "due_date", "priority", "completed"]}

    # Перевіряємо завдання в базі
    existing_task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not existing_task:
        return jsonify({"error": "Task not found"}), 404

    # Оновлюємо завдання в Trello
    trello_id = existing_task.get("trello_task_id")
    if trello_id:
        trello_response = update_trello_task(trello_id, update_data)
        if trello_response.get("error"):
            return jsonify(trello_response), 500

    # Оновлюємо завдання в базі
    tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})
    updated_task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    return jsonify(serialize_task(updated_task)), 200

# Ендпоінт для отримання завдань із Trello
@app.route('/api/trello/tasks/<list_id>', methods=['GET'])
def get_trello_tasks(list_id):
    url = f"https://api.trello.com/1/lists/{list_id}/cards"
    params = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            tasks = response.json()
            return jsonify(tasks), 200
        else:
            return jsonify({"error": "Failed to fetch tasks from Trello"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error fetching tasks from Trello: {str(e)}"}), 500

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if not ObjectId.is_valid(task_id):
        return jsonify({"error": "Invalid task ID"}), 400

    existing_task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not existing_task:
        return jsonify({"error": "Task not found"}), 404

    # Видаляємо завдання з Trello
    trello_id = existing_task.get("trello_task_id")
    if trello_id:
        delete_trello_task(trello_id)

    # Видаляємо завдання з бази даних
    tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return jsonify({"message": "Task deleted successfully"}), 200


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
            return {"error": f"Trello error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Trello sync failed: {str(e)}"}


def update_trello_task(trello_id, update_data):
    url = f"https://api.trello.com/1/cards/{trello_id}"
    params = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    }
    data = {
        "name": update_data.get("title"),
        "desc": update_data.get("description"),
        "due": update_data.get("due_date"),
    }
    response = requests.put(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Trello update failed: {response.status_code}"}


def delete_trello_task(trello_id):
    url = f"https://api.trello.com/1/cards/{trello_id}"
    params = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    }
    try:
        app.logger.debug(f"Attempting to delete task with Trello ID: {trello_id}")
        response = requests.delete(url, params=params)
        if response.status_code == 200:
            app.logger.debug(f"Task with ID {trello_id} deleted successfully from Trello.")
            return True
        else:
            app.logger.error(f"Failed to delete task with ID {trello_id} from Trello: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        app.logger.error(f"Error deleting task with ID {trello_id} from Trello: {str(e)}")
        return False

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
