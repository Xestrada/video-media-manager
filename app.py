from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import boto3
import boto3.s3
from botocore.handlers import disable_signing
import pymysql
import os

# Setup App
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])  # Should change based on is in Development or Production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app)

# Start Database
db = SQLAlchemy(app)

# Enable Variable Port for Heroku
port = int(os.environ.get('PORT', 33507))

# Import models
from models import Actor, ActorMovie, ActorsTVShow
from media_models import Genre
from media_models import Movie, MovieGenre
from media_models import TVShows, TVShowGenre

# Force pymysql to be used as replacement for MySQLdb
pymysql.install_as_MySQLdb()


# Update Movies based on movies in Amazon S3
@app.route('/movies')
def refreshMovies():

    conn = boto3.resource('s3')
    conn.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    bucket = conn.Bucket('videovault4800')

    movie_dict = bucket.objects.filter(Prefix='movies/')
    for item in movie_dict:
        # If the movie path contains a movie title
        if item.key != 'movies/':
            movie_name = item.key.replace('movies/', '').replace('.mp4', '')
            movie_url = 'https://s3.amazonaws.com/videovault4800/' + item.key
            movie_url = movie_url.replace(" ", "+")
            movie_data = Movie.query.filter_by(title=movie_name).first()
            movie_data.url = movie_url
            db.session.commit()
            return 'Added proper url'

    return "End"


@app.route('/tv_shows')
def refresh_tv_shows():
    conn = boto3.resource('s3')
    conn.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    bucket = conn.Bucket('videovault4800')

    tv_show_dict = bucket.objects.filter(Prefix='shows/')
    for title in tv_show_dict:
        # If the shows path contains a tv show title
        if title.key != 'shows/':
            tvs_title = title.key.split("shows/")[1][:-1]
            tvs_season_prefix = 'shows/{}'.format(tvs_title)
            tv_show_season_dict = bucket.objects.filter(Prefix=tvs_season_prefix)

            for season in tv_show_season_dict:
                if season.key != tvs_season_prefix:
                    # Update Episode Url here
                    return None


if __name__ == '__main__':
    app.run(port=port)
