from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.config import Config  # Make sure to import from the correct location

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)  # Use the Config class directly
    
    # Initialize extensions
    db.init_app(app)

    # Register Blueprints here
    from app.controllers.webhook_controller import webhook_bp
    from app.controllers.problem_controller import problem_bp
    from app.controllers.audit_controller import  audit_bp
    from app.controllers.remediation_controller import remediation_bp
    
    app.register_blueprint(webhook_bp)
    app.register_blueprint(problem_bp)
    app.register_blueprint(remediation_bp)
    app.register_blueprint(audit_bp)

    return app
