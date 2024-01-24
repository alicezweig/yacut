from http import HTTPStatus

from flask import jsonify, request, url_for

from yacut import app
from yacut.error_handlers import InvalidRequest
from yacut.models import URLMap


ERROR_MESSAGES = {
    'not_found': 'Указанный id не найден',
    'no_request_body': 'Отсутствует тело запроса',
    'required_field': '\"url\" является обязательным полем!',
}


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.get_urlmap(short_id)
    if not url_map:
        raise InvalidRequest('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})


@app.route('/api/id/', methods=['POST'])
def add_custom_id():
    short_link = ''
    data = request.get_json()
    if not data:
        raise InvalidRequest(ERROR_MESSAGES['no_request_body'])
    if not data.get('url'):
        raise InvalidRequest(ERROR_MESSAGES['required_field'])
    custom_id = data.get('custom_id')
    try:
        url_map = URLMap.create(
            url=data.get('url'), custom_id=custom_id, is_data_valid=False
        )
        short_link = url_for('index', _external=True) + url_map.short
    except Exception as error:
        return jsonify({'message': str(error)}), HTTPStatus.BAD_REQUEST
    return jsonify(
        {'url': url_map.original, 'short_link': short_link}
    ), HTTPStatus.CREATED
