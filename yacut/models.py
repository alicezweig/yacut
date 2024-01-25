import re
from datetime import datetime
from random import choices

from wtforms.validators import ValidationError

from yacut import db
from yacut.error_handlers import CollisionError
from yacut.settings import (ALLOWED_CHARS, AUTO_SHORT_LENGTH,
                            SHORT_REGEX, GENERATE_SHORT_MAX_ATTEMPTS,
                            MAX_SHORT_LENGTH, MAX_ORIGINAL_LENGTH)


DOUBLE_SHORT = 'Предложенный вариант короткой ссылки уже существует.'
UNABLE_TO_CREATE = 'Невозможно создать уникальный ID для короткой ссылки'
VALIDATION_ORIGINAL_ERROR = 'URL не может длинее чем %d символов'
VALIDATION_SHORT_ERROR = 'Указано недопустимое имя для короткой ссылки'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get(short):
        return db.session.query(URLMap).filter_by(short=short).first()

    @staticmethod
    def create_short():
        for _ in range(GENERATE_SHORT_MAX_ATTEMPTS):
            short = ''.join(choices(ALLOWED_CHARS, k=AUTO_SHORT_LENGTH))
            if not URLMap.get(short):
                return short
        raise CollisionError(UNABLE_TO_CREATE)

    @staticmethod
    def create(original, short=None, is_data_valid=False):
        if not (is_data_valid or len(original) <= MAX_ORIGINAL_LENGTH):
            raise ValidationError(
                VALIDATION_ORIGINAL_ERROR.format(MAX_ORIGINAL_LENGTH)
            )
        if not short:
            short = URLMap.create_short()
            is_data_valid = True
        if not is_data_valid:
            if not (len(short) <= MAX_SHORT_LENGTH
                    and re.fullmatch(SHORT_REGEX, short)):
                raise ValidationError(VALIDATION_SHORT_ERROR)
            if URLMap.get(short):
                raise CollisionError(DOUBLE_SHORT)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def to_dict(self):
        return dict(
            original=self.original,
            short=self.short,
        )
