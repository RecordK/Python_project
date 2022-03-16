from flask import Flask, render_template, request, blueprints
from routes.job_route import bp as mov_bp
from routes.mov_route import bp as job_bp
from routes.card_route import bp as card_bp
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)  # 웹 어플리케이션
app.register_blueprint(mov_bp)
app.register_blueprint(job_bp)
app.register_blueprint(card_bp)
app.secret_key = 'asfaf'  # 세션


@app.route('/')  # 요청 url 등록
def root():
    return render_template('index.html')


@app.route('/ref')  # 요청 url 등록
def ref():
    return render_template('ref.html')


if __name__ == '__main__':
    app.run(debug=True)
