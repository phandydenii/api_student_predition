2️⃣ Use Alembic (recommended for production)

Alembic is the official database migration tool for SQLAlchemy.

Install Alembic:

pip install alembic


Initialize Alembic:

alembic init alembic


This creates an alembic/ folder and alembic.ini.

Configure alembic.ini:

sqlalchemy.url = sqlite:///./test.db  # your DB path


Create a migration script:

alembic revision --autogenerate -m "add new column to Student"


Alembic will detect changes in your SQLAlchemy models and generate SQL for SQLite.

Apply migration:

alembic upgrade head


✅ This way, your existing data is preserved, and your database schema is updated.