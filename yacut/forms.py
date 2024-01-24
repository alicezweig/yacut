from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp, ValidationError

from yacut.settings import CUSTOM_ID_REGEX, MAX_CUSTOM_ID_LENGTH, MAX_URL_LENTH
from yacut.models import URLMap

MESSAGES = {
    'long_url': 'Длинная ссылка',
    'short_id': 'Ваш вариант короткой ссылки',
    'data_required_error_message': 'Введите URL.',
    'url_is_valid_error_message': 'Введите действительный URL адрес.',
    'length_error_message': 'Длина ссылки не может превышать %(max)d символов.',
    'regex_error_message': 'Можно использовать только цифры и буквы латинского алфавита.',
    'create_button': 'Создать',
    'double_custom_id': 'Предложенный вариант короткой ссылки уже существует.'
}


class URLForm(FlaskForm):
    original_link = URLField(
        MESSAGES['long_url'],
        validators=[
            DataRequired(message=MESSAGES['data_required_error_message']),
            URL(message=MESSAGES['url_is_valid_error_message']),
            Length(
                max=MAX_URL_LENTH,
                message=MESSAGES['length_error_message'])
        ])
    custom_id = StringField(
        MESSAGES['short_id'],
        validators=[
            Optional(strip_whitespace=False),
            Length(
                max=MAX_CUSTOM_ID_LENGTH,
                message=MESSAGES['length_error_message']
            ),
            Regexp(
                regex=CUSTOM_ID_REGEX,
                message=MESSAGES['regex_error_message']
            )
        ])
    submit = SubmitField(MESSAGES['create_button'])

    def validate_custom_id(self, custom_id):
        if URLMap.get_urlmap(custom_id.data):
            raise ValidationError(MESSAGES['double_custom_id'])