import os

class Config:
    pass

class TestConfig(Config):
    pass

class DevConfig(Config):
    SQLALCHEMY_DB_URI='postgresql+psycopg2://cwilv:iamcwilv@localhost/watchlist'
    Debug=True

class ProdConfig(Config):
    SQLALCHEMY_ALCHEMY_DB_URI=os.environ.get('DB_URL')

config_options={
    'development':DevConfig,
    'production':ProdConfig,
    'test':TestConfig
}
