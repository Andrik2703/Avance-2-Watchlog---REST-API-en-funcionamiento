from src.database import db
from sqlalchemy.orm import relationship

class Series(db.Model):
    __tablename__ = 'series'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    genre = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relación con Season
    seasons = relationship('Season', back_populates='series', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'release_year': self.release_year,
            'genre': self.genre,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'seasons_count': len(self.seasons),
            'total_episodes': sum(season.episode_count for season in self.seasons)
        }