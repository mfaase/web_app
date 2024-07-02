@echo off
rmdir /S /Q migrations
del /Q instance\site.db
del /Q uploads\*
del /Q __pycache__\*
pip install -r requirements.txt
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python add_initial_data.py
echo Reset completed.
pause