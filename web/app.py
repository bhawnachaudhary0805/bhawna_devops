from flask import Flask, jsonify
from celery import Celery
import psycopg2
import os

app = Flask(__name__)

# Celery Configuration
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

@app.route("/")
def index():
    return jsonify({
        "message": "Hello, Bhawna Chaudhary & 2022BCD0059",
        "bio": "I am a student at IIITK."
    })

@app.route("/task")
def run_task():
    task = async_task.delay()
    return jsonify({"task_id": task.id, "status": "Task started!"})

@celery.task
def async_task():
    return "Async task completed!"

@app.route("/users")
def get_users():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
