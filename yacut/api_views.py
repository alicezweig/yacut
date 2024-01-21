from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidRequest
from yacut.constants import YACUT_URL
from yacut.models import URLMap
from yacut.create_short import create_short, get_urlmap, validate_short


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = get_urlmap(short_id)
    if not url_map:
        raise InvalidRequest('Указанный id не найден', 404)
    return jsonify({'url': url_map.original})


@app.route('/api/id/', methods=['POST'])
def add_custom_id():
    data = request.get_json()
    if not data:
        raise InvalidRequest('Отсутствует тело запроса')
    if not data.get('url'):
        raise InvalidRequest('\"url\" является обязательным полем!')
    custom_id = data.get('custom_id')
    if not bool(custom_id):
        custom_id = create_short()
        data['custom_id'] = custom_id
    else:
        if not validate_short(custom_id):
            raise InvalidRequest('Указано недопустимое имя для короткой ссылки')
    if get_urlmap(custom_id):
        raise InvalidRequest(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(
        {'url': url_map.original, 'short_link': YACUT_URL + custom_id}
    ), 201
