from flask import Blueprint, request, jsonify
from src.database import db
from src.models.series import Series
from src.models.seasons import Season

series_bp = Blueprint('series', __name__)

class SeriesService:
    @staticmethod
    def get_all_series():
        """Obtener todas las series"""
        return Series.query.all()
    
    @staticmethod
    def get_series_by_id(series_id):
        """Obtener serie por ID"""
        series = Series.query.get(series_id)
        if not series:
            return None
        return series
    
    @staticmethod
    def create_series(series_data):
        """Crear nueva serie"""
        # Validar campos requeridos
        required_fields = ['title']
        for field in required_fields:
            if field not in series_data:
                return None
        
        series = Series(
            title=series_data['title'],
            description=series_data.get('description', ''),
            release_year=series_data.get('release_year'),
            genre=series_data.get('genre', '')
        )
        
        db.session.add(series)
        db.session.commit()
        return series
    
    @staticmethod
    def update_series(series_id, series_data):
        """Actualizar serie existente"""
        series = Series.query.get(series_id)
        if not series:
            return None
        
        # Actualizar campos permitidos
        allowed_fields = ['title', 'description', 'release_year', 'genre']
        for field in allowed_fields:
            if field in series_data:
                setattr(series, field, series_data[field])
        
        db.session.commit()
        return series
    
    @staticmethod
    def delete_series(series_id):
        """Eliminar serie"""
        series = Series.query.get(series_id)
        if not series:
            return False
        
        db.session.delete(series)
        db.session.commit()
        return True
    
    @staticmethod
    def get_series_with_seasons(series_id):
        """Obtener serie con temporadas (datos normalizados)"""
        series = Series.query.get(series_id)
        if not series:
            return None
        
        # Crear respuesta normalizada
        series_data = series.to_dict()
        series_data['seasons'] = [season.to_dict() for season in series.seasons]
        
        return series_data

class SeasonService:
    @staticmethod
    def create_season(series_id, season_data):
        """Crear nueva temporada"""
        # Validar campos requeridos
        required_fields = ['season_number', 'episode_count']
        for field in required_fields:
            if field not in season_data:
                return None
        
        # Verificar que la serie existe
        series = Series.query.get(series_id)
        if not series:
            return None
        
        season = Season(
            series_id=series_id,
            season_number=season_data['season_number'],
            title=season_data.get('title', f'Season {season_data["season_number"]}'),
            episode_count=season_data['episode_count'],
            release_year=season_data.get('release_year')
        )
        
        db.session.add(season)
        db.session.commit()
        return season
    
    @staticmethod
    def update_season(season_id, season_data):
        """Actualizar temporada existente"""
        season = Season.query.get(season_id)
        if not season:
            return None
        
        # Actualizar campos permitidos
        allowed_fields = ['season_number', 'title', 'episode_count', 'release_year']
        for field in allowed_fields:
            if field in season_data:
                setattr(season, field, season_data[field])
        
        db.session.commit()
        return season
    
    @staticmethod
    def delete_season(season_id):
        """Eliminar temporada"""
        season = Season.query.get(season_id)
        if not season:
            return False
        
        db.session.delete(season)
        db.session.commit()
        return True

# Endpoints de Series
@series_bp.route('/series', methods=['GET'])
def get_series():
    """Obtener todas las series"""
    series_list = SeriesService.get_all_series()
    return jsonify([series.to_dict() for series in series_list])

@series_bp.route('/series/<int:series_id>', methods=['GET'])
def get_series_detail(series_id):
    """Obtener serie con temporadas (datos normalizados)"""
    series_data = SeriesService.get_series_with_seasons(series_id)
    if not series_data:
        return jsonify({'error': 'Series not found'}), 404
    return jsonify(series_data)

@series_bp.route('/series', methods=['POST'])
def create_series():
    """Crear nueva serie"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    series = SeriesService.create_series(data)
    if not series:
        return jsonify({'error': 'Invalid data or missing required fields'}), 400
    
    return jsonify(series.to_dict()), 201

@series_bp.route('/series/<int:series_id>', methods=['PUT'])
def update_series(series_id):
    """Actualizar serie existente"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    series = SeriesService.update_series(series_id, data)
    if not series:
        return jsonify({'error': 'Series not found'}), 404
    
    return jsonify(series.to_dict())

@series_bp.route('/series/<int:series_id>', methods=['DELETE'])
def delete_series(series_id):
    """Eliminar serie"""
    success = SeriesService.delete_series(series_id)
    if not success:
        return jsonify({'error': 'Series not found'}), 404
    
    return '', 204

# Endpoints de Temporadas
@series_bp.route('/series/<int:series_id>/seasons', methods=['POST'])
def create_season(series_id):
    """Crear nueva temporada"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    season = SeasonService.create_season(series_id, data)
    if not season:
        return jsonify({'error': 'Invalid data, missing required fields, or series not found'}), 400
    
    return jsonify(season.to_dict()), 201

@series_bp.route('/seasons/<int:season_id>', methods=['PUT'])
def update_season(season_id):
    """Actualizar temporada existente"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    season = SeasonService.update_season(season_id, data)
    if not season:
        return jsonify({'error': 'Season not found'}), 404
    
    return jsonify(season.to_dict())

@series_bp.route('/seasons/<int:season_id>', methods=['DELETE'])
def delete_season(season_id):
    """Eliminar temporada"""
    success = SeasonService.delete_season(season_id)
    if not success:
        return jsonify({'error': 'Season not found'}), 404
    
    return '', 204