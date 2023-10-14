import os


class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")
    UP_KEY = os.getenv("UP_KEY", "no-hist-key")
    FRONTEND_KEY = os.getenv("FRONTEND_KEY", "no-frontend-key")
    UP_DB = os.getenv("UP_DB", "no-hist-db")
    FRONTEND_DB = os.getenv("FRONTEND_DB", "no-frontend-db")
    URL_DB = os.getenv("MYSQLHOST", "no-url-db")
    PORT_DB = os.getenv("MYSQLPORT", "no-port-db")


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
