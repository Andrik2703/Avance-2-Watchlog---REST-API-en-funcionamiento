from src.database import db
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint

class WatchEntry(db.Model):
    __tablename__ = 'watch_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # 'movie' o 'series'
    content_id = db.Column(db.Integer, nullable=False)  # ID de movie o series
    status = db.Column(db.String(20), nullable=False)  # 'pending', 'watching', 'completed'
    current_progress = db.Column(db.Integer, default=0)  # minutos vistos o episodios vistos
    total_duration = db.Column(db.Integer, nullable=False)  # duración total en minutos o episodios
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # Relaciones
    user = relationship('User', back_populates='watch_entries')
    movie = relationship('Movie', back_populates='watch_entries')
    
    # Restricción de check para status
    __table_args__ = (
        CheckConstraint(
            status.in_(['pending', 'watching', 'completed']), 
            name='check_status'
        ),
        CheckConstraint(
            content_type.in_(['movie', 'series']), 
            name='check_content_type'
        ),
    )
    
    @property
    def percentage_watched(self):
        """Calcula el porcentaje de progreso"""
        if self.total_duration == 0:
            return 0
        return round((self.current_progress / self.total_duration) * 100, 2)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content_type': self.content_type,
            'content_id': self.content_id,
            'status': self.status,
            'current_progress': self.current_progress,
            'total_duration': self.total_duration,
            'percentage_watched': self.percentage_watched,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_progress(self, progress, total_duration=None):
        """Actualiza el progreso y calcula el estado"""
        self.current_progress = progress
        
        if total_duration:
            self.total_duration = total_duration
        
        # Actualizar estado basado en el progreso
        if self.current_progress == 0:
            self.status = 'pending'
        elif self.current_progress >= self.total_duration:
            self.status = 'completed'
            self.current_progress = self.total_duration
        else:
            self.status = 'watching'