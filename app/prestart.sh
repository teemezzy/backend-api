! /usr/bin/env bash

# Let the DB start
python /app/app/before_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/app/initial_data.py
