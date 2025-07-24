from flask import Blueprint

bp = Blueprint('main', __name__)

from . import main_views, question_views, answer_views, auth_views

bp.register_blueprint(main_views.bp)
bp.register_blueprint(question_views.bp)
bp.register_blueprint(answer_views.bp)
bp.register_blueprint(auth_views.bp)

def register_sensor_views():
    from . import sensor_views
    bp.register_blueprint(sensor_views.bp)
