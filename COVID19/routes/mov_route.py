from flask import Blueprint, render_template, request, session
from web_hello.member.vo import Member
from web_hello.member.service import MemberService
from web_hello.bus_info.service import Service
from web_hello.bus_info.vo import Bus

bp = Blueprint('movie', __name__, url_prefix='/movie')
service = MemberService()
bus_service = Service()


@bp.route('/')
def movie():
    return render_template('movie.html')


@bp.route('/join')  # 요청 url 등록
def joinForm():
    # 회원가입 양식 폼만 준다
    return render_template('member/join.html')


@bp.route('/join', methods=['POST'])  # 요청 url 등록
def join():
    # 회원가입 양식에 작성하고 가입버튼 누른 요청 가입 완료
    id = request.form['id']
    m: Member = service.getById(id)
    if m is None:
        pwd = request.form['pwd']
        name = request.form['name']
        email = request.form['email']
        service.addMember(Member(id, pwd, name, email))
        return render_template('index.html')
    else:
        msg = '있는 아이디 입니다.'
        return render_template('error.html', msg=msg)


@bp.route('/login')
def loginForm():
    return render_template('member/login.html')


@bp.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    pwd = request.form['pwd']
    m: Member = service.getById(id)
    if m is None:
        msg = '없는 아이디 입니다.'
        return render_template('error.html', msg=msg)
    else:
        if pwd == m.pwd:
            session['flag'] = True
            session['loginid'] = id
            session['name'] = m.name
            # {{session.loginid}} 이런식으로 접근
            myinfo = m
        else:
            msg = '패스워드가 일치하지 않습니다. 다시 한 번 확인해주세요.'
            return render_template('error.html', msg=msg)
    return render_template('member/myinfo.html', myinfo=myinfo)


@bp.route('/myinfo')
def myinfo():
    id = session['loginid']
    m: Member = service.getById(id)
    if m is None:
        msg = '잘못된 접근입니다.'
        return render_template('error.html', msg=msg)
    else:
        myinfo = m
    return render_template('member/myinfo.html', myinfo=myinfo)


@bp.route('/editmyinfo')
def editmyinfoForm():
    return render_template('member/editmyinfo.html')


@bp.route('/editmyinfo', methods=['POST'])  # 요청 url 등록
def editmyinfo():
    id = session['loginid']
    pwd = request.form['pwd']
    name = request.form['name']
    email = request.form['email']
    service.editMember(Member(id, pwd, name, email))
    m: Member = service.getById(id)
    myinfo = m

    return render_template('member/myinfo.html', myinfo=myinfo)


@bp.route('/logout')
def logout():
    session['flag'] = False
    session['loginid'] = ''
    return render_template('index.html')


@bp.route('/delmem')
def delmemForm():
    return render_template('member/delmem.html')


@bp.route('/delmem', methods=['POST'])
def delmem():
    id = session['loginid']
    pwd = request.form['pwd']
    m: Member = service.getById(id)
    if pwd == m.pwd:
        service.delMember(id)
        session['flag'] = False
        session['loginid'] = ''
    return render_template('index.html')


@bp.route('/mybus', methods=['POST', 'GET'])  # 요청 url 등록
def mybus():
    id = session['loginid']
    res = bus_service.myBusList(id)

    if res == []:
        msg = '저장된 버스가 없습니다.'
        return render_template('member/mybus.html', res=msg, flag=False)
    return render_template('member/mybus.html', res=res, flag=True)

# 로그인하면 내가 등록한 버스 목록을 볼 수 있다.
#  1 자주 사용 버스 등록 등록 폼에 버스 이름을 입력. 검색을 해서  없는 버스면 없다.
# 있는 버스면 결과페이지 정보추출해서 db에저장
