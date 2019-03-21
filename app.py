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


    for item in bucket.objects.filter(Prefix='movies/'):
        if item.key != 'movies/':
            movieName = item.key.replace('movies/', '').replace('.mp4', '')
            movieURL = 'https://s3.amazonaws.com/videovault4800/' + item.key
            movieURL = movieURL.replace(" ", "+")
            movieData = Movie.query.filter_by(title=movieName).first()
            movieData.url = movieURL
            db.session.commit()
            return 'Added propor url'

    return "End"



if __name__ == '__main__':
    app.run(port=port)
