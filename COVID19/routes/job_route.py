from flask import Blueprint, render_template, request, session
from job.service import JobService

bp = Blueprint('job', __name__, url_prefix='/job')
service = JobService()

@bp.route('/')
def job():
    return render_template('job.html')
