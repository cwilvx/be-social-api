import os

class Config:
    MONGO_URI="mongodb+srv://{user}:{pswd}@cluster0.vte2d.mongodb.net/{db}?retryWrites=true&w=majority".format(
        user = os.environ.get('MONGO_USER'),
        pswd = os.environ.get('MONGO_PSWD'),
        db = os.environ.get('MONGO_DB')
    )

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
