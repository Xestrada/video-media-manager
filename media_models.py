from app import db

class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    genre_type = db.Column(db.VARCHAR)

    def __init__(self, genre_type):
        self.title = genre_type

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'genre_type': self.genre_type
        }


# Models Regarding the movies Database
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR)
    year = db.Column(db.VARCHAR)
    service = db.Column(db.VARCHAR)
    tag = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    date_added = db.Column(db.Date)
    image_url = db.Column(db.VARCHAR)
    description = db.Column(db.TEXT)
    avg_rating = db.Column(db.REAL)

    def __init__(self, title, year, service, tag, url, date_added, image_url, description, avg_rating):
        self.title = title
        self.year = year
        self.service = service
        self.tag = tag
        self.url = url
        self.date_added = date_added
        self.image_url = image_url
        self.description = description
        self.avg_rating = avg_rating

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'service': self.service,
            'tag': self.tag,
            'url': self.url,
            'date_added': self.date_added,
            'image_url': self.image_url,
            'avg_rating': self.avg_rating,
        }


class MovieGenre(db.Model):
    __tablename__ = 'movie_genre'

    movie_id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, movie_id, genre_id):
        self.movie_id = movie_id
        self.genre_id = genre_id

    def __repr__(self):
        return '<movie_id {} genre_id {}>'.format(self.movie_id, self.genre_id)


class MovieInfo:
    def __init__(self, title, year, description, stars, genres, image_url, avg_rating):
        self.title = title
        self.year = year
        self.description = description
        self.stars = stars
        self.genres = genres
        self.image_url = image_url
        self.avg_rating = avg_rating

    def serialize(self):
        return {
            'title': self.title,
            'year': self.year,
            'description': self.description,
            'stars': self.stars,
            'genres': self.genres,
            'image_url': self.image_url,
            'avg_rating': self.avg_rating,
        }


class TVShows(db.Model):
    __tablename__ = 'tv_shows'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR)
    year = db.Column(db.VARCHAR)
    num_seasons = db.Column(db.INTEGER)
    num_episodes = db.Column(db.INTEGER)
    service = db.Column(db.VARCHAR)
    tag = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    date_added = db.Column(db.Date)
    image_url = db.Column(db.VARCHAR)
    description = db.Column(db.TEXT)
    avg_rating = db.Column(db.REAL)

    def __init__(self, title, year, num_seasons, num_episodes, service, tag, url, date_added, image_url, description,
                 avg_rating):
        self.title = title
        self.year = year
        self.num_seasons = num_seasons
        self.num_episodes = num_episodes
        self.service = service
        self.tag = tag
        self.url = url
        self.date_added = date_added
        self.image_url = image_url
        self.description = description
        self.avg_rating = avg_rating

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'num_seasons': self.num_seasons,
            'num_episodes': self.num_episodes,
            'service': self.service,
            'tag': self.tag,
            'url': self.url,
            'date_added': self.date_added,
            'image_url': self.image_url,
            'avg_rating': self.avg_rating,
        }


class TVShowGenre(db.Model):
    __tablename__ = 'tv_show_genre'

    tv_show_id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, tv_show_id, genre_id):
        self.tv_show_id = tv_show_id
        self.genre_id = genre_id

    def __repr__(self):
        return '<tv_show_id {} genre_id {}'.format(self.tv_show_id, self.genre_id)


class TVShowSeasons(db.Model):
    __tablename__ = 'tv_show_season_episodes'

    tv_show_id = db.Column(db.INTEGER, primary_key=True)
    season = db.Column(db.INTEGER, primary_key=True)
    num_episodes = db.Column(db.INTEGER)

    def __init__(self, num_episodes):
        self.num_episodes = num_episodes
        self.episodes = self.get_episodes()


class TVShowSeasonInfo:
    def __init__(self, season, episodes):
        self.season = season
        self.episodes = episodes

    def serialize(self):
        return {
            'season': self.season,
            'episodes': [ep.serialize() for ep in self.episodes],
        }


class TVShowEpisodes(db.Model):
    __tablename__ = 'tv_show_episodes'

    tv_show_id = db.Column(db.INTEGER, primary_key=True)
    season_id = db.Column(db.INTEGER, primary_key=True)
    episode = db.Column(db.INTEGER, primary_key=True)
    episode_name = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)

    def __init__(self, episode_name):
        self.episode_name = episode_name

    def serialize(self):
        return {
            'episode': self.episode,
            'episode_name': self.episode_name,
            'url': self.url,
        }


class TVShowInfo:
    def __init__(self, title, year, description, season_info, stars, genres, image_url, avg_rating):
        self.title = title
        self.year = year
        self.description = description
        self.season_info = season_info
        self.stars = stars
        self.genres = genres
        self.image_url = image_url
        self.avg_rating = avg_rating

    def serialize(self):
        return {
            'title': self.title,
            'year': self.year,
            'description': self.description,
            'season_info': [season.serialize() for season in self.season_info],
            'stars': self.stars,
            'genres': self.genres,
            'image_url': self.image_url,
            'avg_rating': self.avg_rating
        }
