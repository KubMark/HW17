# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from create_data import Movie, Director, Genre

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


api = Api(app)
movie_ns = api.namespace("movies")
director_ns = api.namespace("directors")
genre_ns = api.namespace("genres")


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


# ========= Movies ==========
@movie_ns.route("/")
class MoviesViews(Resource):

    def get(self):
        global all_movies
        if not request.args:
            all_movies = db.session.query(Movie).all()
        else:
            director_id = request.args.get("director_id")
            genre_id = request.args.get("genre_id")

            if director_id is not None and genre_id is not None:
                all_movies = Movie.query.filter(Movie.director_id == director_id and Movie.genre_id == genre_id).all()

            elif director_id is not None:
                all_movies = Movie.query.filter(Movie.director_id == director_id).all()

            elif genre_id is not None:
                all_movies = Movie.query.filter(Movie.genre_id == genre_id).all()

        return movies_schema.dump(all_movies), 200

    def post(self):
        request_json = request.json

        new_movie = Movie(**request_json)

        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route("/<int:uid>")
class MovieViews(Resource):
    def get(self, uid:int):
        try:
            movie = db.session.query(Movie).get(uid)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, uid:int):
        try:
            request_json = request.json

            movie = db.session.query(Movie).get(uid)
            movie.id = request_json.get("id")
            movie.title = request_json.get("title")
            movie.description = request_json.get("description")
            movie.trailer = request_json.get("trailer")
            movie.year = request_json.get("year")
            movie.rating = request_json.get("rating")
            movie.genre_id = request_json.get("genre_id")
            movie.director_id = request_json.get("director_id")

            db.session.add(movie)
            db.session.commit()
            return "", 204
        except Exception as e:
            return str(e), 404

    def delete(self, uid:int):
        movie = db.session.query(Movie).get(uid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204


# ======= Directors =========
@director_ns.route("/")
class DirectorsViews(Resource):

    def get(self):
        directors = db.session.query(Director).all()
        return directors_schema.dump(directors), 200

    def post(self):
        request_json = request.json

        new_director = Director(**request_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@director_ns.route("/<int:uid>")
class DirectorViews(Resource):
    def get(self, uid:int):
        try:
            director = db.session.query(Director).get(uid)
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404

    def put(self, uid:int):
        try:
            request_json = request.json

            director = db.session.query(Director).get(uid)
            director.id = request_json.get("id")
            director.name = request_json.get("name")

            db.session.add(director)
            db.session.commit()
            return "", 204
        except Exception as e:
            return str(e), 404

    def delete(self, uid:int):
        director = db.session.query(Director).get(uid)
        db.session.delete(director)
        db.session.commit()
        return "", 204


# ======= Genres ======
@genre_ns.route("/")
class GenresViews(Resource):

    def get(self):
        genres = db.session.query(Genre).all()
        return genres_schema.dump(genres), 200

    def post(self):
        request_json = request.json

        new_genre = Genre(**request_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genre_ns.route("/<int:uid>")
class GenreViews(Resource):
    def get(self, uid:int):
        try:
            genre = db.session.query(Genre).get(uid)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

    def put(self, uid:int):
        try:
            request_json = request.json
            genre = db.session.query(Genre).get(uid)
            genre.id = request_json.get("id")
            genre.name = request_json.get("name")

            db.session.add(genre)
            db.session.commit()
            return "", 204
        except Exception as e:
            return str(e), 404

    def delete(self, uid:int):
        genre = db.session.query(Genre).get(uid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)