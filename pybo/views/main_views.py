from flask import Blueprint, url_for, current_app

from werkzeug.utils import redirect
from pybo.models import db

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    current_app.logger.info("INFO 레벨로 출력")
    return redirect(url_for('question._list'))


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)