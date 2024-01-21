from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import URL, DataRequired, Length, Regexp

from yacut.constants import CUSTOM_ID_REGEX, MAX_CUSTOM_ID_LENGTH, MAX_URL_LENTH


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Введите URL.'),
            URL(message='Введите действительный URL адрес.'),
            Length(
                max=MAX_URL_LENTH,
                message='Длина ссылки не может превышать %(max)d символов.')
        ])
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                max=MAX_CUSTOM_ID_LENGTH,
                message='Длина ссылки не может превышать %(max)d символов.'
            ),
            Regexp(
                regex=CUSTOM_ID_REGEX,
                message='Можно использовать только цифры и буквы латинского алфавита.'
            )
        ])
    submit = SubmitField('Создать')