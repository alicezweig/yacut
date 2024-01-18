import string
from random import choices

from yacut import db
from yacut.constants import MAX_CUSTOM_ID_LENGTH
from yacut.models import URLMap


def create_short():
    short = ''.join(
        choices(string.ascii_letters + string.digits, k=MAX_CUSTOM_ID_LENGTH)
    )
    if db.session.query(URLMap).filter_by(short=short).scalar():
        create_short()
    return short