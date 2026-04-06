import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-super-secret-key-change-in-production'
    
    # Better: Store database inside 'instance' folder (recommended for Flask)
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'study_groups.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True