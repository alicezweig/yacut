from flask import abort, Markup, flash, redirect, render_template

from yacut import app, db
from yacut.constants import YACUT_URL
from yacut.create_short import create_short, get_urlmap
from yacut.forms import URLForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        if get_urlmap(custom_id):
            flash(u'Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        if not custom_id:
            custom_id = create_short()
        db.session.add(URLMap(original=original_link, short=custom_id))
        db.session.commit()
        flash(
            Markup(
                f'Ваша короткая ссылка: <a href="{YACUT_URL}{custom_id}">'
                f'{YACUT_URL}{custom_id}</a>'
            )
        )
    return render_template('index.html', form=form)


@app.route('/<custom_id>', methods=['GET'])
def redirect_to_original(custom_id):
    url_map = get_urlmap(custom_id)
    if url_map:
        return redirect(url_map.original, code=302)
    abort(404)