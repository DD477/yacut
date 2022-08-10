import random
import string
from http import HTTPStatus

from flask import flash, redirect, render_template

from . import app, db
from .constaints import LEN_AUTO_SHORT_URL, NAME_IS_BUSY
from .forms import YacutForm
from .models import URL_map


def get_unique_short_id():
    """Генерирует уникальные короткие ссылки."""
    short_link = ''.join(random.choices(
        string.ascii_letters + string.digits, k=LEN_AUTO_SHORT_URL)
    )
    if URL_map.query.filter_by(short=short_link).first():
        short_link = get_unique_short_id()
    return short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if form.validate_on_submit():
        short_name = form.custom_id.data
        if URL_map.query.filter_by(short=short_name).first():
            flash(NAME_IS_BUSY.format(short_name))
            return render_template(
                'yacut.html', form=form
            ), HTTPStatus.BAD_REQUEST
        if short_name is None or short_name == '':
            short_name = get_unique_short_id()
        url_map = URL_map(
            original=form.original_link.data,
            short=short_name,
        )
        db.session.add(url_map)
        db.session.commit()

        return render_template(
            'yacut.html', form=form, short=short_name
        ), HTTPStatus.OK
    return render_template('yacut.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    url = URL_map.query.filter_by(short=short).first_or_404()
    return redirect(url.original)
