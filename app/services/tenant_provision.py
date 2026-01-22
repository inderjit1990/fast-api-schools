from sqlalchemy import text
from app.core.database import engine, Base
from app.config.tenant_tables import TENANT_TABLES

def create_tenant_schema(schema_name: str):
    """
    1. Create schema if not exists
    2. Create all tenant tables inside schema
    """

    with engine.begin() as conn:
        # 1️⃣ Create schema
        conn.execute(
            text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
        )


    # 2️⃣ Create all tables inside the new schema
    with engine.connect() as conn:
        for table in TENANT_TABLES:
            conn.execute(
                text(
                    f"""
                    CREATE TABLE IF NOT EXISTS "{schema_name}".{table}
                    (LIKE public.{table} INCLUDING ALL)
                    """
                )
            )
        conn.commit()

    print(f"✅ Tables copied to schema: {schema_name}")

    return True
