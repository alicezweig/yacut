import re
from datetime import datetime
from random import choices

from wtforms.validators import ValidationError

from yacut import db
from yacut.error_handlers import CollisionError
from yacut.settings import (ALLOWED_CHARS, AUTO_CUSTOM_ID_LENGTH,
                            CUSTOM_ID_REGEX, GENERATE_SHORT_MAX_ATTEMPTS,
                            MAX_CUSTOM_ID_LENGTH, MAX_URL_LENTH)

ERROR_MESSAGES = {
    'unable_to_create': 'Невозможно создать уникальный ID для короткой ссылки',
    'double_short': 'Предложенный вариант короткой ссылки уже существует.',
    'validation_error': 'Указано недопустимое имя для короткой ссылки',
}


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_URL_LENTH), nullable=False)
    short = db.Column(db.String(MAX_CUSTOM_ID_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_urlmap(custom_id):
        return db.session.query(URLMap).filter_by(short=custom_id).first()

    @classmethod
    def create(cls, url, custom_id=None, is_data_valid=False):
        if not bool(custom_id):
            for _ in range(GENERATE_SHORT_MAX_ATTEMPTS):
                custom_id = ''.join(
                    choices(ALLOWED_CHARS, k=AUTO_CUSTOM_ID_LENGTH)
                )
                if not cls.get_urlmap(custom_id):
                    is_data_valid = True
                    break
            else:
                raise CollisionError(ERROR_MESSAGES['unable_to_create'])
        if not is_data_valid:
            if not (len(custom_id) <= MAX_CUSTOM_ID_LENGTH
                    and re.fullmatch(CUSTOM_ID_REGEX, custom_id)):
                raise ValidationError(ERROR_MESSAGES['validation_error'])
            if cls.get_urlmap(custom_id):
                raise CollisionError(ERROR_MESSAGES['double_short'])
        url_map = cls(original=url, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )
