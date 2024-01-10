from flask import render_template

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url_map = URLMap(
            original=form.url.data,
            short=form.custom_id.data
        )
        db.session.add(url_map)
        db.session.commit()
    return render_template('index.html', form=form)