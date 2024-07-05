@echo off
rmdir /S /Q migrations
del /Q instance\site.db
del /Q uploads\*
del /Q __pycache__\*
python add_initial_data.py
echo Reset completed.
pause