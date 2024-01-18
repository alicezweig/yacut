from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Regexp

from yacut.constants import MAX_CUSTOM_ID_LENGTH, MAX_URL_LENTH


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
            ),
            Regexp(
                regex='^$|[0-9A-Za-z]',
                message='Можно использовать только цифры и буквы латинского алфавита.'
            )
        ])
    submit = SubmitField('Создать')