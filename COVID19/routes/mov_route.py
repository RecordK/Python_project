from flask import Blueprint, render_template, request, session
from movie.service import MovieService

bp = Blueprint('movie', __name__, url_prefix='/movie')
service = MovieService()


@bp.route('/')
def movie():
    return render_template('movie.html')

@bp.route('/review')
def review():
    return render_template('review.html')

@bp.route('/genre')
def genre():
    return render_template('genre.html')

@bp.route('/review-test2', methods=['POST'])
def test3():
    level = service.review_test()
    print(level)
    return render_template('result2.html', level=level)

@bp.route('/review-test', methods=['POST'])
def test2():
    data = str(request.form['review'])
    level = service.read_review(data)
    print(level)
    return render_template('result2.html', level=level)

@bp.route('/genre-test', methods=['POST'])
def test1():
    data = str(request.form['summary'])
    levels = service.genre_test(data)
    print(levels)
    return render_template('result.html', levels=levels)

