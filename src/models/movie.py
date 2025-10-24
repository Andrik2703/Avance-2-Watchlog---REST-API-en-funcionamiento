from src.database import db
from sqlalchemy.orm import relationship

class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    duration = db.Column(db.Integer)  # en minutos
    genre = db.Column(db.String(100))
    director = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relación con WatchEntry
    watch_entries = relationship('WatchEntry', back_populates='movie')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'release_year': self.release_year,
            'duration': self.duration,
            'genre': self.genre,
            'director': self.director,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }