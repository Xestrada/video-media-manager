import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'key'
    SQLALCHEMY_DATABASE_URI = os.environ['AWS_RDS_URL']
    POSTS_PER_PAGE = 5  # How many items to display per page (for pagination)
    RECENT_TIME = 30  # How many days to consider recently added


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
