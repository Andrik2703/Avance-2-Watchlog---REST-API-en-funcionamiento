from src.database import db
from sqlalchemy.orm import relationship

class Season(db.Model):
    __tablename__ = 'seasons'
    
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    season_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200))
    episode_count = db.Column(db.Integer, nullable=False)
    release_year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relaciones
    series = relationship('Series', back_populates='seasons')
    
    def to_dict(self):
        return {
            'id': self.id,
            'series_id': self.series_id,
            'season_number': self.season_number,
            'title': self.title,
            'episode_count': self.episode_count,
            'release_year': self.release_year,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }