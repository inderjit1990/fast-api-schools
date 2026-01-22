from app.core.celery_app import celery_app
from app.services.tenant_provision import create_tenant_schema


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def provision_tenant_schema(self, schema_name: str):
    """
    Background task to provision tenant schema
    """
    create_tenant_schema(schema_name)
    return f"Schema {schema_name} provisioned successfully"
