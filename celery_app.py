from celery import Celery
from settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

# The broker URL can point to Redis or RabbitMQ
# For simplicity, we can use a local Redis instance.
# Example: "redis://localhost:6379/0"
# You need to have Redis installed and running.
# As a fallback for local dev, we can use a file-system-based broker,
# but it's not recommended for production.
# For this example, let's assume Redis is running.

app = Celery(
    "ai-illustrate",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["tasks"],  # Points to the tasks module
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

if __name__ == "__main__":
    app.start()
