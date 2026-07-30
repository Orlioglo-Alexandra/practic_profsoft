# AI Task Service

Микросервис для обработки AI-задач через REST API.

## Запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Docker:

```bash
docker build -t ai-task-service .
docker run -p 8000:8000 ai-task-service
```
