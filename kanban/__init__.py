from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import config


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)    
    
    # Model    
    from . import task_models

    # Blueprint
    from . import kanban_views
    app.register_blueprint(kanban_views.bp)

    return app
