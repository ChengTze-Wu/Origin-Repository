class Config:
    # Base Config
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    TEMPLATES_AUTO_RELOAD = True


class DevConfig(Config):
    ENV = 'development'
    TESTING = True
    DEBUG = True


class ProConfig(Config):
    ENV = 'production'
    TESTING = False
    DEBUG = False
