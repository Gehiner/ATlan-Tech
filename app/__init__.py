from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask import Flask, session, render_template

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()  

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)

    from app.routes import main
    from app.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    from app.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.context_processor
    def cantidad_carrito():
        carrito = session.get('carrito', {})
        total_items = sum(carrito.values())
        return dict(total_items=total_items)
    return app

