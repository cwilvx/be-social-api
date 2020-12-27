import os

class Config:
    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    pass

class DevConfig(Config):
    MONGO_URI="mongodb+srv://{user}:{pswd}@cluster0.vte2d.mongodb.net/<dbname>?retryWrites=true&w=majority".format(
        user = os.environ.get('MONGO_USER'),
        pswd = os.environ.get('MONGO_PSWD')
    )

    DEBUG=True

class ProdConfig(Config):
    pass

config_options={
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}

# MODE = os.environ.get('MODE')
