import os
import re

import boto3
import boto3.s3
import pymysql
from botocore.handlers import disable_signing
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

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
from media_models import Movie
from media_models import TVShows, TVShowEpisodes

# Force pymysql to be used as replacement for MySQLdb
pymysql.install_as_MySQLdb()


# Update Movies based on movies in Amazon S3
@app.route('/movies')
def refresh_movies():
    result = list()
    conn = boto3.resource('s3')
    conn.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    bucket = conn.Bucket('videovault4800')

    movie_dict = bucket.objects.filter(Prefix='movies/')
    for item in movie_dict:

        # Ex. movies/Bird Box.mp4
        if item.key != 'movies/':
            movie_name = item.key.replace('movies/', '').replace('.mp4', '')
            movie_url = 'https://s3.amazonaws.com/videovault4800/' + item.key
            movie_url = movie_url.replace(" ", "+")
            movie_data = Movie.query.filter_by(title=movie_name).first()
            movie_data.url = movie_url
            db.session.commit()
            result.append('Added proper url to {}'.format(movie_name))

    return jsonify({'result': [r for r in result]})


# Update TV Shows based on TV Shows in Amazon S3
@app.route('/tv_shows')
def refresh_tv_shows():
    result = list()
    conn = boto3.resource('s3')
    conn.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    bucket = conn.Bucket('videovault4800')

    tv_show_dict = bucket.objects.filter(Prefix='shows/')
    for show in tv_show_dict:

        # Ex. shows/game of thrones
        if matches_show_pattern(show.key):
            tvs_title = show.key.split("shows/")[1][:-1]
            tvs_season_prefix = 'shows/{}'.format(tvs_title)
            tv_show_season_dict = bucket.objects.filter(Prefix=tvs_season_prefix)

            for season in tv_show_season_dict:
                season = season.key.split(tvs_season_prefix)[1][1:-1]

                # Ex. shows/game of thrones/season 1
                if matches_season_pattern(season):
                    season_id = season[-1]
                    season_episode_prefix = '{}/{}/'.format(tvs_season_prefix, season)
                    season_episode_dict = bucket.objects.filter(Prefix=season_episode_prefix)

                    for episode in season_episode_dict:
                        episode = episode.key.split(season_episode_prefix)[1][:-1]

                        # Ex. shows/game of thrones/season 1/episode 1
                        if matches_episode_pattern(episode):
                            episode_id = episode[-1]
                            episode_video_prefix = '{}/{}/{}/'.format(tvs_season_prefix, season, episode)

                            video_dict = bucket.objects.filter(Prefix=episode_video_prefix)
                            for video in video_dict:

                                # Ex. shows/game of thrones/season 1/episode 1/Winter Is Coming.mp4
                                if video.key != episode_video_prefix:
                                    tv_show_id = TVShows.query.filter_by(title=tvs_title).first().id
                                    set_episode_url(tv_show_id, season_id, episode_id, video.key)
                                    result.append("{} S{} E{} url added.".format(tvs_title, season_id, episode_id))

    return jsonify({'result': [r for r in result]})


# Adds the URL of a specific TV Show's Season's Episode to the tv_show_episodes Table
def set_episode_url(tv_show_id: int, season_id: int, episode_id: int, path: str) -> None:
    episode_data = TVShowEpisodes.query \
        .filter_by(tv_show_id=tv_show_id) \
        .filter_by(season_id=season_id) \
        .filter_by(episode=episode_id) \
        .first()

    episode_url = 'https://s3.amazonaws.com/videovault4800/' + path
    episode_url = episode_url.replace(' ', '+')
    episode_data.url = episode_url
    db.session.commit()


# show/[anything]
def matches_show_pattern(show: str) -> bool:
    shows_pattern = re.compile("shows/+?")
    return shows_pattern.match(show) is not None


# season [any num]
def matches_season_pattern(season: str) -> bool:
    season_pattern = re.compile("season [0-9]+$")
    return season_pattern.match(season) is not None


# episode [any num]$
def matches_episode_pattern(episode: str) -> bool:
    episode_pattern = re.compile("episode [0-9]+$")
    return episode_pattern.match(episode) is not None


if __name__ == '__main__':
    app.run(port=port)
