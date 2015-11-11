@echo off
color 03

python _4fortune/manage.py runserver 0.0.0.0:8000 --noreload

echo . & pause
