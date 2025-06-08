#!/bin/bash

echo "✅ Appliquer les migrations Django..."
python manage.py migrate --noinput

echo "✅ Collecter les fichiers statiques..."
python manage.py collectstatic --noinput

echo "🚀 Lancer Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 core.wsgi:application
