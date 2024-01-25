from http import HTTPStatus

from flask import jsonify, request, url_for
from wtforms.validators import ValidationError

from yacut import app
from yacut.error_handlers import InvalidRequest, CollisionError
from yacut.models import URLMap
from yacut.settings import REDIRECT_URL_NAME

GENERAL_ERROR = 'Случилась ошибка: %s'
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
        return jsonify(
            {
                'url': data['url'],
                'short_link': url_for(
                    REDIRECT_URL_NAME,
                    short=URLMap.create(
                        original=data['url'],
                        short=short,
                        is_data_valid=False
                    ).short,
                    _external=True
                )}
        ), HTTPStatus.CREATED
    except (CollisionError, ValidationError) as error:
        raise InvalidRequest(str(error))
    except Exception as error:
        app.logger.exception(GENERAL_ERROR, error)
        raise InvalidRequest(str(error), 500)
