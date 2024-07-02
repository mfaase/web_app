#!/bin/bash
rm -rf migrations
rm -f instance/site.db
rm -f uploads/*
rm -rf __pycache__
pip install -r requirements.txt
# flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade
python add_initial_data.py
echo "Reset completed."