from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .constaints import (MAX_LEN_ORIGINAL_URL, MAX_LEN_SHORT_URL, MIN_LEN_URL,
                         REG_PATTERN)


class YacutForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(
                MIN_LEN_URL, MAX_LEN_ORIGINAL_URL,
                message='Длина ссылка не более 300 символов'),
            URL(message='Некорректный URL адрес'),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                MIN_LEN_URL, MAX_LEN_SHORT_URL,
                message='Длина ссылка не более 16 символов'),
            Regexp(REG_PATTERN,
                   message=(
                       'Допускаются только буквы латинского алфавита и цифры')
                   ),
            Optional(),
        ]
    )
    submit = SubmitField('Создать')
