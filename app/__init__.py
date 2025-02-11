from flask import Flask
from flask_login import LoginManager
from .core import main
from dotenv import load_dotenv
from .models import db, Users,Audios
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

    @app.before_request
    def _initialize_db():
        if db.is_closed():
            db.connect()
        db.create_tables([Users,Audios], safe=True)  
        db.close()

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    app.register_blueprint(main)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.get_or_none(Users.id == int(user_id))

    return app