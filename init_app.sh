#!/bin/bash
pip install -r requirements.txt
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python add_initial_data.py
echo "Initialization completed."