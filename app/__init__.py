from flask import Flask
from flask_marshmallow import Marshmallow
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import config

# ACA SE REGISTRAN LAS RUTAS ? (punto 6)
#from app.resources import account
#from app.resources import coin
#from app.resources import wallet
#from app.resources import role
#from app.resources import swap


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app() -> None:
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    
    from app.resources import home
    app.register_blueprint(home, url_prefix='/api/v1')
    
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app
