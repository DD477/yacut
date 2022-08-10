from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constaints import ID_NOT_FOUND
from .error_handlers import InvalidAPIUsage, request_verification
from .models import URL_map


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short(short_id):
    url = URL_map.query.filter_by(short=short_id).first()
    if url is not None:
        return jsonify({'url': url.original}), HTTPStatus.OK
    raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    custom_id = request_verification(data)
    url = URL_map(original=data['url'], short=custom_id)
    db.session.add(url)
    db.session.commit()
    return jsonify(
        {'url': data['url'], 'short_link': f'{request.url_root}{custom_id}'}
    ), HTTPStatus.CREATED
