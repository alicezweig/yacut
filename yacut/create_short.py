import string
import re
from random import choices

from yacut import db
from yacut.constants import (AUTO_CUSTOM_ID_LENGTH, CUSTOM_ID_REGEX,
                             MAX_CUSTOM_ID_LENGTH)
from yacut.models import URLMap


def get_urlmap(custom_id):
    return db.session.query(URLMap).filter_by(short=custom_id).first()


def create_short():
    custom_id = ''.join(
        choices(string.ascii_letters + string.digits, k=AUTO_CUSTOM_ID_LENGTH)
    )
    if get_urlmap(custom_id):
        create_short()
    return custom_id


def validate_short(custom_id):
    return (re.fullmatch(CUSTOM_ID_REGEX, custom_id)
            and len(custom_id) <= MAX_CUSTOM_ID_LENGTH)