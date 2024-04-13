from flask import Blueprint, request, jsonify
from src import db

movies_blueprint = Blueprint('movies', __name__)

# Create a new movie
@movies_blueprint.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    try:
        theater_location = data['theater_location']
        name = data['name']
        overall_rating = data['overall_rating']
        genre = data['genre']
        activity_type_id = data['activity_type_id']

        query = '''
            INSERT INTO Movies (TheaterLocation, Name, OverallRating, Genre, Activity_Type_ID) 
            VALUES (%s, %s, %s, %s, %s)
        '''
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute(query, (theater_location, name, overall_rating, genre, activity_type_id))
        conn.commit()

        return jsonify({"message": "Movie created successfully.", "id": cur.lastrowid}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred creating the movie."}), 500

# Retrieve all movies
@movies_blueprint.route('/movies', methods=['GET'])
def get_all_movies():
    try:
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM Movies')
        movies = cur.fetchall()

        return jsonify(movies), 200
    except Exception as e:
        return jsonify({"error": "An error occurred fetching the movies."}), 500

# Retrieve a single movie by ID
@movies_blueprint.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    try:
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM Movies WHERE MovieID = %s', (movie_id,))
        movie = cur.fetchone()

        if movie:
            return jsonify(movie), 200
        else:
            return jsonify({"error": "Movie not found."}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred fetching the movie."}), 500

# Update a movie
@movies_blueprint.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    data = request.get_json()
    try:
        theater_location = data['theater_location']
        name = data['name']
        overall_rating = data['overall_rating']
        genre = data['genre']
        activity_type_id = data['activity_type_id']

        query = '''
            UPDATE Movies 
            SET TheaterLocation = %s, Name = %s, OverallRating = %s, Genre = %s, Activity_Type_ID = %s 
            WHERE MovieID = %s
        '''
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute(query, (theater_location, name, overall_rating, genre, activity_type_id, movie_id))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"error": "Movie not found."}), 404

        return jsonify({"message": "Movie updated successfully."}), 200
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred updating the movie."}), 500

# Delete a movie
@movies_blueprint.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    try:
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM Movies WHERE MovieID = %s', (movie_id,))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"error": "Movie not found."}), 404

        return jsonify({"message": "Movie deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred deleting the movie."}), 500

# Register the blueprint in your app configuration
# app.register_blueprint(movies_blueprint, url_prefix='/api')
