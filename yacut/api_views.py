from flask import jsonify, request
from marshmallow import ValidationError

from yacut import app, db
from yacut.constants import YACUT_URL
from yacut.models import URLMap
from yacut.schemas import URLMapSchema
from yacut.create_short import create_short


@app.route('/api/id/<custom_id>/', methods=['GET'])
def get_original_url(custom_id):
    urlmap = db.session.query(URLMap).filter_by(custom_id=custom_id).scalar()
    if urlmap:
        return jsonify({'url': URLMapSchema().dump(urlmap).get('url')})
    return jsonify({'message': 'Указанный id не найден'}), 404


@app.route('/api/id/', methods=['POST'])
def add_custom_id():
    schema = URLMapSchema()
    data = request.get_json()
    custom_id = data.get('custom_id')
    if not custom_id:
        data['custom_id'] = create_short()
    try:
        result = schema.load(data)
    except ValidationError as error:
        return jsonify({'message': list(*error.messages.values()).pop()}), 400
    if db.session.query(URLMap).filter_by(custom_id=custom_id).scalar():
        return jsonify({'message': 'Предложенный вариант короткой ссылки уже существует.'}), 400
    db.session.add(result)
    db.session.commit()
    response = {
        'url': data['url'],
        'short_link': YACUT_URL + data['custom_id']
    }
    return jsonify(response), 201
