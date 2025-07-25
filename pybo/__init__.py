from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from markdown import markdown
from markupsafe import Markup

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def page_not_found(e):
    return render_template('404.html'), 404


def register_sensor_views():
    from pybo.views import sensor_views
    app.register_blueprint(sensor_views.bp)

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    app.register_error_handler(404, page_not_found)

    from pybo.views import main_views, question_views, answer_views, auth_views, sensor_views

    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(sensor_views.bp)  # 여기서 바로 등록

    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    def markdown_filter(text):
        html = markdown(text, extensions=['fenced_code', 'codehilite'])
        return Markup(html)
    app.jinja_env.filters['markdown'] = markdown_filter

    return app
