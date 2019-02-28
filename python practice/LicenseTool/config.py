class Config(object):
    DEBUG = True
    SECRET_KEY = 'admin'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://licensetool:licensetool@localhost/licensetool'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
