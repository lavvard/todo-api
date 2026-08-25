from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "/data/todos.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

@app.route("/todos", methods=["GET"])
def list_todos():
    conn = get_db()
    rows = conn.execute("SELECT * FROM todos").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify(error="title is required"), 400
    conn = get_db()
    cur = conn.execute("INSERT INTO todos (title) VALUES (?)", (data["title"],))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify(id=new_id, title=data["title"], done=False), 201

@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify(error="not found"), 404
    return jsonify(dict(row))

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    conn = get_db()
    conn.execute(
        "UPDATE todos SET title = COALESCE(?, title), done = COALESCE(?, done) WHERE id = ?",
        (data.get("title"), data.get("done"), todo_id),
    )
    conn.commit()
    conn.close()
    return jsonify(status="updated")

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_db()
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return jsonify(status="deleted")

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)