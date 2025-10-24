from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    # Importar modelos para que SQLAlchemy los reconozca
    from src.models.user import User
    from src.models.movie import Movie
    from src.models.series import Series
    from src.models.seasons import Season
    from src.models.watch_entry import WatchEntry
    
    # Registrar blueprints
    from src.api.movies import movies_bp
    from src.api.series import series_bp
    from src.api.progress import progress_bp
    
    app.register_blueprint(movies_bp, url_prefix='/api')
    app.register_blueprint(series_bp, url_prefix='/api')
    app.register_blueprint(progress_bp, url_prefix='/api')
    
    # Crear tablas en la base de datos
    with app.app_context():
        db.create_all()
        
        # Crear usuario demo si no existe
        demo_user = User.query.filter_by(username='demo').first()
        if not demo_user:
            demo_user = User(username='demo', email='demo@example.com')
            db.session.add(demo_user)
            db.session.commit()
    
    return app