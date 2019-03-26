from app import db


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.VARCHAR)
    first_name = db.Column(db.VARCHAR)
    last_name = db.Column(db.VARCHAR)

    def __init__(self, full_name, first_name, last_name):
        self.full_name = full_name
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }


class ActorMovie(db.Model):
    __tablename__ = 'movie_actors'

    movie_id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def _repr__(self):
        return '<movie_id {} actor_id {}>'.format(self.movie_id, self.actor_id)

    def serialize(self):
        return {
            'movie_id': self.movie_id,
            'actor_id': self.actor_id,
        }


class ActorsTVShow(db.Model):
    __tablename__ = 'tv_show_actors'

    tv_show_id = db.Column(db.Integer, primary_key=True)
    actors_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, tv_show_id, actors_id):
        self.tv_show_id = tv_show_id
        self.actors_id = actors_id

    def _repr__(self):
        return '<tv_show_id {} actors_id {}>'.format(self.tv_show_id, self.actors_id)

    def serialize(self):
        return {
            'tv_show_id': self.tv_show_id,
            'actors_id': self.actors_id,
        }
