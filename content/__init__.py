from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    #CONFIGURACIOMN DEL PROYECTO
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = ["dev"],
        SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
    )

    db.init_app(app)

    # REGUSTAR Blueprint
    from . import todo
    from . import auth
    app.register_blueprint(todo.frontPage)
    app.register_blueprint(auth.authentication)


    @app.route('/')
    def index():
        return render_template('index.html')

    with app.app_context():
        db.create_all()

    return app
