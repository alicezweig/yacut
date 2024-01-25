from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from yacut import app
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.settings import REDIRECT_URL_NAME

GENERAL_ERROR = 'Случилась ошибка: %s'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original = form.original_link.data
    short = form.custom_id.data
    try:
        return render_template(
            'index.html',
            form=form,
            context={
                'short': url_for(
                    endpoint=REDIRECT_URL_NAME,
                    short=URLMap.create(
                        original=original,
                        short=short,
                        is_data_valid=True
                    ).short,
                    _external=True
                )})
    except Exception as error:
        flash(str(error))
        app.logger.exception(GENERAL_ERROR, error)


@app.route('/<short>', methods=['GET'])
def redirect_to_original(short):
    url_map = URLMap.get(short)
    if url_map:
        return redirect(url_map.original, code=HTTPStatus.FOUND)
    abort(HTTPStatus.NOT_FOUND)
