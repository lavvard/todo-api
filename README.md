# Описание

простое REST API приложение для управления задачами (to-do list), написанное на Flask с использованием SQLite. упаковано в Docker с использованием volumes для персистентности данных.

# Стек

- Python / Flask
- SQLite
- Docker
- Ansible
- CI/CD GHA (позже)

# Эндпоинты

- `GET /todos` — список всех задач
- `POST /todos` — создать задачу
- `GET /todos/<id>` — получить задачу по id
- `PUT /todos/<id>` — обновить задачу
- `DELETE /todos/<id>` — удалить задачу
- `GET /health` — проверка работоспособности

# Запуск

```bash
docker build -t todo-api .
docker run -d -p 5000:5000 -v todo-api-data:/data todo-api
```

Данные сохраняются в Docker volume `todo-api-data`, поэтому переживают пересоздание контейнера.
