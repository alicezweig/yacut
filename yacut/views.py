from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from yacut import app
from yacut.forms import URLForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index():
    short_link = ''
    form = URLForm()
    if form.validate_on_submit():
        url = form.original_link.data
        custom_id = form.custom_id.data
        try:
            url_map = URLMap.create(
                url=url, custom_id=custom_id, is_data_valid=True
            )
            short_link = url_for('index', _external=True) + url_map.short
        except Exception as error:
            flash(str(error))
    return render_template(
        'index.html', form=form, context={'short_link': short_link}
    )


@app.route('/<custom_id>', methods=['GET'])
def redirect_to_original(custom_id):
    url_map = URLMap.get_urlmap(custom_id)
    if url_map:
        return redirect(url_map.original, code=HTTPStatus.FOUND)
    abort(HTTPStatus.NOT_FOUND)
