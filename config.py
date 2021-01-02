import os

class Config:
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
