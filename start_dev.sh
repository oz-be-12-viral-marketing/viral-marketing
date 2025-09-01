#!/bin/bash

# --- Cleanup: Stop any old running services first ---
echo "Stopping any old Celery and Django processes..."
pkill -f "celery -A config"
pkill -f "manage.py runserver"
sleep 2 # Give a moment for processes to terminate

echo "---------------------------------------------"

# The virtual environment is not activated via 'source'.
# Instead, we call the python executable from within the .venv directory directly for robustness.

echo "Starting Celery Worker..."
# Start Celery Worker in the background, logging to a file
nohup .venv/bin/python -m celery -A config worker -l info > celery_worker.log 2>&1 &
echo "Celery Worker started in background. Log: celery_worker.log"

echo "Starting Celery Beat..."
# Start Celery Beat in the background, logging to a file
nohup .venv/bin/python -m celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler > celery_beat.log 2>&1 &
echo "Celery Beat started in background. Log: celery_beat.log"

echo "Starting Django Server..."
# Start Django Development Server in the background, logging to a file
nohup .venv/bin/python manage.py runserver > django_server.log 2>&1 &
echo "Django Server started in background. Log: django_server.log"

echo "---------------------------------------------"
echo "All services started. Use 'ps aux | grep python' or 'ps aux | grep celery' to see processes."
echo "Remember to start Redis server manually if it's not already running."
