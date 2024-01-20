from marshmallow import Schema, fields, post_load, validate, pre_load

from yacut.models import URLMap
from yacut.constants import MAX_CUSTOM_ID_LENGTH


class URLMapSchema(Schema):
    url = fields.Url(
        required=True,
        error_messages={'required': '\"url\" является обязательным полем!'}
    )
    custom_id = fields.String(
        validate=[
            validate.Regexp(
                regex='^$|[0-9A-Za-z]*$',
                error='Указано недопустимое имя для короткой ссылки'
            ),
            validate.Length(
                max=MAX_CUSTOM_ID_LENGTH,
                error='Указано недопустимое имя для короткой ссылки'
            )
        ])

    @pre_load
    def unwrap_envelope(self, data, **kwargs):
        if not data:
            raise validate.ValidationError('Отсутствует тело запроса')
        return data

    @post_load
    def make_url_map(self, data, **kwargs):
        return URLMap(**data)
