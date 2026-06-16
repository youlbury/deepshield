from flask import Flask
from flask_cors import CORS
from routes.api import api_bp
from routes.evidence import evidence_bp
from routes.benchmark import benchmark_bp
from extensions import db
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chovy_evidence.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

    db.init_app(app)
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(evidence_bp, url_prefix='/api')
    app.register_blueprint(benchmark_bp)
    
    with app.app_context():
        db.create_all()
        for folder in ['uploads', 'evidence', 'reports']:
            if not os.path.exists(folder):
                os.makedirs(folder)

    return app

if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0', port=5001)