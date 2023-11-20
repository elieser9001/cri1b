from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
        
    from .endpoints import license
    app.register_blueprint(license.bp)

    return app
