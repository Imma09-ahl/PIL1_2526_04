import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mentorlink_secret_key')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'mentorlink')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
