import re
from random import choices

from yacut import db
from yacut.error_handlers import CollisionError
from yacut.models import URLMap
from yacut.settings import (ALLOWED_CHARS, AUTO_CUSTOM_ID_LENGTH,
                            CUSTOM_ID_REGEX, GENERATE_SHORT_MAX_ATTEMPTS,
                            MAX_CUSTOM_ID_LENGTH)

COLLISION_ERROR_MESSAGE = 'Невозможно создать уникальный ID для короткой ссылки.'


def get_urlmap(custom_id):
    return db.session.query(URLMap).filter_by(short=custom_id).first()


def create_short():
    for _ in range(GENERATE_SHORT_MAX_ATTEMPTS):
        custom_id = ''.join(
            choices(ALLOWED_CHARS, k=AUTO_CUSTOM_ID_LENGTH)
        )
        if not get_urlmap(custom_id):
            return custom_id
    raise CollisionError(COLLISION_ERROR_MESSAGE)


def validate_short(custom_id):
    return (len(custom_id) <= MAX_CUSTOM_ID_LENGTH
            and re.fullmatch(CUSTOM_ID_REGEX, custom_id))
