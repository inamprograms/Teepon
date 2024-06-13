# Function to register the API routes 
def register_routes(app):
    from src.routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')
