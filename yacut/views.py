from flask import flash, render_template

from yacut import app, db
from yacut.constants import YACUT_URL
from yacut.create_short import create_short
from yacut.forms import URLForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        original = form.url.data
        short = form.custom_id.data
        if db.session.query(URLMap).filter_by(short=short).scalar():
            flash('Такая короткая ссылка уже занята.')
            flash('Введите другое значение или оставьте поле пустым, \
                  чтобы сервис сгенерировал ссылку автоматически.')
            return render_template('index.html', form=form)
        if not short:
            short = create_short()
        db.session.add(URLMap(original=original, short=short))
        db.session.commit()
        flash(f'Ваша короткая ссылка: {YACUT_URL}{short}')
    return render_template('index.html', form=form)