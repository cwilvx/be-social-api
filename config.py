import os

class Config:
    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    pass

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://cwilv:iamcwilv@localhost/social_app_0'
    DEBUG=True

class ProdConfig(Config):
    SQLALCHEMY_ALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')

config_options={
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}

MODE = os.environ.get('MODE')
