from flask import Blueprint, request, jsonify
from src.database import db
from src.models.watch_entry import WatchEntry
from src.models.movie import Movie
from src.models.series import Series
from src.models.user import User

progress_bp = Blueprint('progress', __name__)

def get_user_id():
    """Obtiene y valida el user_id del header X-User-Id"""
    user_id = request.headers.get('X-User-Id')
    if not user_id:
        return None
    
    try:
        user_id = int(user_id)
        # Verificar que el usuario existe
        user = User.query.get(user_id)
        return user_id if user else None
    except (ValueError, TypeError):
        return None

class ProgressService:
    @staticmethod
    def get_watchlist(user_id):
        """Obtener la watchlist completa del usuario"""
        return WatchEntry.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_watch_entry(entry_id, user_id):
        """Obtener una entrada específica de la watchlist"""
        return WatchEntry.query.filter_by(id=entry_id, user_id=user_id).first()
    
    @staticmethod
    def add_to_watchlist(user_id, content_data):
        """Añadir contenido a la watchlist"""
        content_type = content_data.get('content_type')
        content_id = content_data.get('content_id')
        
        # Validar campos requeridos
        if not content_type or not content_id:
            return None
        
        # Validar tipo de contenido
        if content_type not in ['movie', 'series']:
            return None
        
        # Verificar que el contenido existe
        if content_type == 'movie':
            content = Movie.query.get(content_id)
            if not content:
                return None
            total_duration = content.duration
        else:  # series
            content = Series.query.get(content_id)
            if not content:
                return None
            # Para series, la duración total es el número total de episodios
            total_duration = sum(season.episode_count for season in content.seasons)
        
        # Verificar si ya existe en la watchlist
        existing_entry = WatchEntry.query.filter_by(
            user_id=user_id, 
            content_type=content_type, 
            content_id=content_id
        ).first()
        
        if existing_entry:
            return existing_entry
        
        # Crear nueva entrada
        watch_entry = WatchEntry(
            user_id=user_id,
            content_type=content_type,
            content_id=content_id,
            status='pending',
            current_progress=0,
            total_duration=total_duration
        )
        
        db.session.add(watch_entry)
        db.session.commit()
        return watch_entry
    
    @staticmethod
    def update_progress(entry_id, user_id, progress_data):
        """Actualizar el progreso de visualización"""
        watch_entry = WatchEntry.query.filter_by(id=entry_id, user_id=user_id).first()
        if not watch_entry:
            return None
        
        current_progress = progress_data.get('current_progress')
        if current_progress is not None:
            # Validar que el progreso no sea negativo
            if current_progress < 0:
                return None
            
            # Usar el método helper para actualizar progreso y estado
            watch_entry.update_progress(current_progress)
        
        db.session.commit()
        return watch_entry
    
    @staticmethod
    def remove_from_watchlist(entry_id, user_id):
        """Eliminar contenido de la watchlist"""
        watch_entry = WatchEntry.query.filter_by(id=entry_id, user_id=user_id).first()
        if not watch_entry:
            return False
        
        db.session.delete(watch_entry)
        db.session.commit()
        return True

# Endpoints
@progress_bp.route('/watchlist', methods=['GET'])
def get_watchlist():
    """Obtener la watchlist del usuario"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Valid X-User-Id header is required'}), 401
    
    watchlist = ProgressService.get_watchlist(user_id)
    return jsonify([entry.to_dict() for entry in watchlist])

@progress_bp.route('/watchlist', methods=['POST'])
def add_to_watchlist():
    """Añadir contenido a la watchlist"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Valid X-User-Id header is required'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    watch_entry = ProgressService.add_to_watchlist(user_id, data)
    if not watch_entry:
        return jsonify({'error': 'Invalid data, missing required fields, or content not found'}), 400
    
    return jsonify(watch_entry.to_dict()), 201

@progress_bp.route('/watchlist/<int:entry_id>/progress', methods=['PUT'])
def update_progress(entry_id):
    """Actualizar progreso de visualización"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Valid X-User-Id header is required'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    watch_entry = ProgressService.update_progress(entry_id, user_id, data)
    if not watch_entry:
        return jsonify({'error': 'Watch entry not found or invalid progress value'}), 404
    
    return jsonify(watch_entry.to_dict())

@progress_bp.route('/watchlist/<int:entry_id>', methods=['DELETE'])
def remove_from_watchlist(entry_id):
    """Eliminar contenido de la watchlist"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Valid X-User-Id header is required'}), 401
    
    success = ProgressService.remove_from_watchlist(entry_id, user_id)
    if not success:
        return jsonify({'error': 'Watch entry not found'}), 404
    
    return '', 204

@progress_bp.route('/watchlist/<int:entry_id>', methods=['GET'])
def get_watch_entry(entry_id):
    """Obtener una entrada específica de la watchlist"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Valid X-User-Id header is required'}), 401
    
    watch_entry = ProgressService.get_watch_entry(entry_id, user_id)
    if not watch_entry:
        return jsonify({'error': 'Watch entry not found'}), 404
    
    return jsonify(watch_entry.to_dict())