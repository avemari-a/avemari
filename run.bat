@echo off
call venv\Scripts\activate
python init_db.py
set FLASK_APP=app.py
flask run
