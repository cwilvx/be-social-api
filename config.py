import os, datetime

class Config:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_EXPIRATION_DELTA = datetime.timedelta(days=10)
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=10)

    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    pass

class DevConfig(Config):
    DEBUG=True

class ProdConfig(Config):
    pass

config_options={
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}
