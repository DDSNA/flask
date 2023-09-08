import os


class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")
    HIST_KEY = os.getenv("HIST_KEY", "no-hist-key")
    FRONTEND_KEY = os.getenv("FRONTEND_KEY", "no-frontend-key")
    HIST_DB = os.getenv("HIST_DB", "no-hist-db")
    FRONTEND_DB = os.getenv("FRONTEND_DB", "no-frontend-db")
class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
