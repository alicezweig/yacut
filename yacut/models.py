from datetime import datetime

from yacut.constants import MAX_URL_LENTH, MAX_CUSTOM_ID_LENGTH
from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_URL_LENTH), nullable=False)
    short = db.Column(db.String(MAX_CUSTOM_ID_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )

    def from_dict(self, data):
        # for field in URLMap.__table__.columns.keys():
        #     if field in data:
        #         setattr(self, field, data[field])
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])
