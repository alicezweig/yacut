from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from yacut import app
from yacut.forms import URLForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    url = form.original_link.data
    custom_id = form.custom_id.data
    try:
        url_map = URLMap.create(
            url=url, custom_id=custom_id, is_data_valid=True
        )
    except Exception as error:
        flash(str(error))
    return render_template(
        'index.html',
        form=form,
        context={'short': url_for('index', _external=True) + url_map.short}
    )


@app.route('/<custom_id>', methods=['GET'])
def redirect_to_original(custom_id):
    url_map = URLMap.get_urlmap(custom_id)
    if url_map:
        return redirect(url_map.original, code=HTTPStatus.FOUND)
    abort(HTTPStatus.NOT_FOUND)
