from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'

db=SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:70778513@localhost:3306/Restaurant"
    app.config['DEBUG']=True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
    app.config['SECRET_KEY']='suibianxie'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    login_manager.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app