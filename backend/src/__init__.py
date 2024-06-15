from flask import Flask
from flask_cors import CORS

def create_app():

    app = Flask(__name__)
    CORS(app)
        
    # Initialize database
    # from src.database.db import connect
    # connect(app).Main.users

    # Register blueprints
    from src.routes import register_routes
    register_routes(app)
    
    return app
