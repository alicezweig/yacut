from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional, Regexp,
                                ValidationError)

from yacut.models import URLMap
from yacut.settings import MAX_ORIGINAL_LENGTH, MAX_SHORT_LENGTH, SHORT_REGEX

LONG_URL = 'Длинная ссылка'
SHORT = 'Ваш вариант короткой ссылки'
DATA_REQUIRED_ERROR_MESSAGE = 'Введите URL.'
URL_IS_VALID_ERROR_MESSAGE = 'Введите действительный URL адрес.'
LENGTH_ERROR_MESSAGE = 'Длина ссылки не может превышать %(max)d символов.'
REGEX_ERROR_MESSAGE = (
    'Можно использовать только цифры и буквы латинского алфавита.'
)
CREATE_BUTTON = 'Создать'
DOUBLE_SHORT = 'Предложенный вариант короткой ссылки уже существует.'


class URLForm(FlaskForm):
    original_link = URLField(
        LONG_URL,
        validators=[
            DataRequired(message=DATA_REQUIRED_ERROR_MESSAGE),
            URL(message=URL_IS_VALID_ERROR_MESSAGE),
            Length(
                max=MAX_ORIGINAL_LENGTH,
                message=LENGTH_ERROR_MESSAGE)
        ])
    custom_id = StringField(
        SHORT,
        validators=[
            Optional(strip_whitespace=False),
            Length(
                max=MAX_SHORT_LENGTH,
                message=LENGTH_ERROR_MESSAGE
            ),
            Regexp(
                regex=SHORT_REGEX,
                message=REGEX_ERROR_MESSAGE
            )
        ])
    submit = SubmitField(CREATE_BUTTON)

    def validate_custom_id(self, short):
        if URLMap.get(short.data):
            raise ValidationError(DOUBLE_SHORT)
