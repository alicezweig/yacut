from flask import jsonify, request
from marshmallow import ValidationError

from yacut import app, db
from yacut.models import URLMap
from yacut.schemas import URLMapSchema


@app.route('/api/id/<custom_id>/', methods=['GET'])
def get_original_url(custom_id):
    urlmap = db.session.query(URLMap).filter_by(custom_id=custom_id).scalar()
    if urlmap:
        return jsonify({'url': URLMapSchema().dump(urlmap).get('url')})
    return jsonify({'message': 'Указанный id не найден'}), 404


@app.route('/api/id/', methods=['POST'])
def add_custom_id():
    schema = URLMapSchema()
    try:
        result = schema.load(request.get_json())
    except ValidationError as error:
        response = {'message': list(*error.messages.values()).pop()}
    else:

        db.session.add(result)
        db.session.commit()
        response = schema.dump(result)
    return jsonify(response), 201
