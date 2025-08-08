set -e

echo "Waiting for PostgreSQL to be ready..."

max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if nc -z db 5432; then
        echo "PostgreSQL is ready on attempt $attempt."
        break
    fi
    
    if [ $attempt -eq $max_attempts ]; then
        echo "PostgreSQL is not ready after $max_attempts attempts. Exiting."
        exit 1
    fi
    
    echo "Attempt $attempt: PostgreSQL not ready yet. Waiting..."
    sleep 2
    attempt=$((attempt + 1))
done

cd /app

echo "📦 Applying migrations..."
if ! alembic -c app/alembic.ini upgrade head; then
    echo "Migration failed!"
    exit 1
fi

echo "Starting FastAPI..."
exec python -m uvicorn app.main:main_app --host 0.0.0.0 --port 8000 --reload