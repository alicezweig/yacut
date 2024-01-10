from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, Length, URL

from yacut.constants import MAX_URL_LENTH, MAX_CUSTOM_ID_LENGTH


class URLForm(FlaskForm):
    url = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Введите URL.'),
            URL(message='Введите действительный URL адрес.'),
            Length(
                max=MAX_URL_LENTH,
                message='Длина ссылки не может превышать %(max)d символов.')
        ])
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                max=MAX_CUSTOM_ID_LENGTH,
                message='Длина ссылки не может превышать %(max)d символов.'
            )
        ])
    submit = SubmitField('Создать')