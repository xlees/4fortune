@echo off
color 0D

python ./manage.py runserver 0.0.0.0:8000
rem python _4fortune/manage.py runserver 0.0.0.0:8000 --noreload

echo . & pause
