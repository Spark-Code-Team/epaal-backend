#!/usr/bin/env bash
set -e

# Activate virtual environment
source /opt/epaal-backend/.venv/bin/activate

# Navigate to project directory
cd /opt/epaal-backend

# Run Django commands
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn EvaamBack.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
