from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(env=None):
    from config import config_by_name
    from flask import Flask

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    
    db.init_app(app)

    return app



app = create_app()
