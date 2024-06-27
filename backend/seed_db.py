import os
from flask import current_app
from .extensions import db

def setup_database():
    setup_sql_path = os.path.join('./application', 'setup.sql')
    if os.path.exists(setup_sql_path):
        print("Executing setup.sql file...")
        with current_app.open_resource(setup_sql_path, 'r') as f:
            setup_sql = f.read()
            db.engine.execute(setup_sql)
        print("Setup.sql executed successfully.")
    else:
        print("setup.sql file not found. Skipping database setup.")

if __name__ == '__main__':
    setup_database()
