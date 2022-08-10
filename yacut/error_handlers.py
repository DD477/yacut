import re
from http import HTTPStatus

from flask import jsonify, render_template

from . import app, db
from .constaints import (API_NAME_IS_BUSY, BAD_NAME, EMPTY_REQUEST,
                         FIELD_IS_REQUIRED)
from .models import URL_map
from .views import get_unique_short_id


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR


def request_verification(data):
    if not data:
        raise InvalidAPIUsage(
            EMPTY_REQUEST, HTTPStatus.BAD_REQUEST
        )
    if not data.get('url'):
        raise InvalidAPIUsage(
            FIELD_IS_REQUIRED, HTTPStatus.BAD_REQUEST
        )
    custom_id = data.get(
        'custom_id', get_unique_short_id()
    )
    if not custom_id:
        custom_id = get_unique_short_id()
    if re.search('[А-Яа-я !@%#.&*+$_{+-]', custom_id) or len(custom_id) >= 16:
        raise InvalidAPIUsage(
            BAD_NAME, HTTPStatus.BAD_REQUEST
        )
    if URL_map.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(
            API_NAME_IS_BUSY.format(custom_id), HTTPStatus.BAD_REQUEST
        )
    return custom_id