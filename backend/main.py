from flask import jsonify
from src import create_app

# Entry point to run the Flask app
app = create_app()

@app.route('/')
def wellcome():
    return "<center><h1> Wellcome to Teepon<h1></center>"

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error' : 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error' : 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')