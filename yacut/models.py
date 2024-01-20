from datetime import datetime

from yacut.constants import MAX_URL_LENTH, MAX_CUSTOM_ID_LENGTH
from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(MAX_URL_LENTH), nullable=False)
    custom_id = db.Column(db.String(MAX_CUSTOM_ID_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
