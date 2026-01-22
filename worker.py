from app.core.celery_app import celery_app
import app.tasks.tenant_tasks
# Auto-discover tasks
celery_app.autodiscover_tasks(["app.tasks"])
