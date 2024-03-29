import os
import string


SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False

AUTO_SHORT_LENGTH = 6
GENERATE_SHORT_MAX_ATTEMPTS = 100
MAX_ORIGINAL_LENGTH = 2048
MAX_SHORT_LENGTH = 16

ALLOWED_CHARS = string.ascii_letters + string.digits
SHORT_REGEX = fr'^[{ALLOWED_CHARS}]*$'

REDIRECT_URL_NAME = 'redirect_to_original'
