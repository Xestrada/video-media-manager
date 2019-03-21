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

    def __init__(self, title, year, service, tag, url, date_added):
        self.title = title
        self.year = year
        self.service = service
        self.tag = tag
        self.url = url
        self.date_added = date_added

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

    def serialize(self):
        return {
            'movie_id': self.movie_id,
            'genre_id': self.genre_id,
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

    def __init__(self, title, year, num_seasons, num_episodes, service, tag, url, date_added):
        self.title = title
        self.year = year
        self.num_seasons = num_seasons
        self.num_episodes = num_episodes
        self.service = service
        self.tag = tag
        self.url = url
        self.date_added = date_added

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

    def serialize(self):
        return {
            'tv_show_id': self.tv_show_id,
            'genre_id': self.genre_id,
        }
