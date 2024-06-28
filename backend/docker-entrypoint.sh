#!/bin/bash
# Make migrations folder
echo "Make migrations folder"
flask db init
echo "Done - 1"

echo "Make migrations"
flask db migrate -m "First migration"
echo "Done - 2"

echo "Apply migrations"
flask db upgrade
echo "Done - 3"

# Start server
echo "Starting app"
flask run --host=0.0.0.0 --port=5000