from http import HTTPStatus

from flask import jsonify, url_for, request

from yacut import app
from yacut.error_handlers import InvalidRequest
from yacut.models import URLMap


NOT_FOUND = 'Указанный id не найден'
NO_REQUEST_BODY = 'Отсутствует тело запроса'
REQUIRED_FIELD = '"url" является обязательным полем!'


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.get(short_id)
    if not url_map:
        raise InvalidRequest(NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})


@app.route('/api/id/', methods=['POST'])
def add_short():
    data = request.get_json()
    if not data:
        raise InvalidRequest(NO_REQUEST_BODY)
    if not data.get('url'):
        raise InvalidRequest(REQUIRED_FIELD)
    short = data.get('custom_id')
    try:
        url_map = URLMap.create(
            original=data.get('url'), short=short, is_data_valid=False
        )
    except Exception as error:
        return jsonify({'message': str(error)}), HTTPStatus.BAD_REQUEST
    return jsonify(
        {
            'url': url_map.original,
            'short_link': url_for(
                'redirect_to_original',
                short=url_map.short,
                _external=True
            )
        }
    ), HTTPStatus.CREATED
