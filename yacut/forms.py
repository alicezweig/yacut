from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from yacut.settings import CUSTOM_ID_REGEX, MAX_CUSTOM_ID_LENGTH, MAX_URL_LENTH

STRINGS = {
    'long_url': 'Длинная ссылка',
    'short_id': 'Ваш вариант короткой ссылки',
    'data_required_error_message': 'Введите URL.',
    'url_is_valid_error_message': 'Введите действительный URL адрес.',
    'length_error_message': 'Длина ссылки не может превышать %(max)d символов.',
    'regex_error_message': (
        'Можно использовать только цифры и буквы латинского алфавита.'
    ),
    'create_button': 'Создать'
}


class URLForm(FlaskForm):
    original_link = URLField(
        STRINGS['long_url'],
        validators=[
            DataRequired(message=STRINGS['data_required_error_message']),
            URL(message=STRINGS['url_is_valid_error_message']),
            Length(
                max=MAX_URL_LENTH,
                message=STRINGS['length_error_message'])
        ])
    custom_id = StringField(
        STRINGS['short_id'],
        validators=[
            Optional(strip_whitespace=False),
            Length(
                max=MAX_CUSTOM_ID_LENGTH,
                message=STRINGS['length_error_message']
            ),
            Regexp(
                regex=CUSTOM_ID_REGEX,
                message=STRINGS['regex_error_message']
            )
        ])
    submit = SubmitField(STRINGS['create_button'])
