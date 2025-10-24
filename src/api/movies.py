from flask import Blueprint, request, jsonify
from src.database import db
from src.models.movie import Movie

movies_bp = Blueprint('movies', __name__)

class MovieService:
    @staticmethod
    def get_all_movies():
        """Obtener todas las películas"""
        return Movie.query.all()
    
    @staticmethod
    def get_movie_by_id(movie_id):
        """Obtener película por ID"""
        movie = Movie.query.get(movie_id)
        if not movie:
            return None
        return movie
    
    @staticmethod
    def create_movie(movie_data):
        """Crear nueva película"""
        # Validar campos requeridos
        required_fields = ['title', 'duration']
        for field in required_fields:
            if field not in movie_data:
                return None
        
        movie = Movie(
            title=movie_data['title'],
            description=movie_data.get('description', ''),
            release_year=movie_data.get('release_year'),
            duration=movie_data['duration'],
            genre=movie_data.get('genre', ''),
            director=movie_data.get('director', '')
        )
        
        db.session.add(movie)
        db.session.commit()
        return movie
    
    @staticmethod
    def update_movie(movie_id, movie_data):
        """Actualizar película existente"""
        movie = Movie.query.get(movie_id)
        if not movie:
            return None
        
        # Actualizar campos permitidos
        allowed_fields = ['title', 'description', 'release_year', 'duration', 'genre', 'director']
        for field in allowed_fields:
            if field in movie_data:
                setattr(movie, field, movie_data[field])
        
        db.session.commit()
        return movie
    
    @staticmethod
    def delete_movie(movie_id):
        """Eliminar película"""
        movie = Movie.query.get(movie_id)
        if not movie:
            return False
        
        db.session.delete(movie)
        db.session.commit()
        return True

# Endpoints
@movies_bp.route('/movies', methods=['GET'])
def get_movies():
    """Obtener todas las películas"""
    movies = MovieService.get_all_movies()
    return jsonify([movie.to_dict() for movie in movies])

@movies_bp.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Obtener película por ID"""
    movie = MovieService.get_movie_by_id(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify(movie.to_dict())

@movies_bp.route('/movies', methods=['POST'])
def create_movie():
    """Crear nueva película"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    movie = MovieService.create_movie(data)
    if not movie:
        return jsonify({'error': 'Invalid data or missing required fields'}), 400
    
    return jsonify(movie.to_dict()), 201

@movies_bp.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    """Actualizar película existente"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    movie = MovieService.update_movie(movie_id, data)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404
    
    return jsonify(movie.to_dict())

@movies_bp.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    """Eliminar película"""
    success = MovieService.delete_movie(movie_id)
    if not success:
        return jsonify({'error': 'Movie not found'}), 404
    
    return '', 204