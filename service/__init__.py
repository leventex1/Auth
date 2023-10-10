from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt

app = Flask(__name__)

class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt()



def create_app():
    app.config.from_envvar('AUTH_SERVICE_CONFIG')

    db.init_app(app)
    bcrypt.init_app(app)

    from service.routes import routes
    app.register_blueprint(routes)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def test():
        return '<h1>Hello Auth!<h1>'

    return app

