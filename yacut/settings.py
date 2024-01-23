import os
import string

# Константы 
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv('SECRET_KEY')

# Константы
MAX_URL_LENTH = 2048
MAX_CUSTOM_ID_LENGTH = 16
AUTO_CUSTOM_ID_LENGTH = 6
GENERATE_SHORT_MAX_ATTEMPTS = 100
ALLOWED_CHARS = string.ascii_letters + string.digits
CUSTOM_ID_REGEX = fr'^[{ALLOWED_CHARS}]*$'