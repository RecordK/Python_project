from flask import Blueprint, Flask, render_template, request, session
from web_hello.bus_info.service import Service
from web_hello.bus_info.vo import Bus

# 버스와 관련된 기능 제공 클래스
bus_service = Service()

# 블루프린트 객체 생성 : 라우트 등록 객체
bp = Blueprint('card', __name__, url_prefix='/card')

@bp.route('/')
def card():
    return render_template('card.html')

@bp.route('/businfo', methods=['POST', 'GET'])  # 요청 url 등록
def businfo():
    busnm = request.form['busnm']  # 폼 양식의 이름이 'busnm'인 요소의 값을 읽음
    res = bus_service.getBusinfoByNm(busnm)
    if res is None:
        msg = '해당 버스는 존재하지 않습니다.'
        return render_template('error.html', msg=msg)
    if busnm == '':
        msg = '버스 번호를 입력해주세요.'
        return render_template('error.html', msg=msg)
    return render_template('bus/busList.html', res=res, flag=True)


@bp.route('/stationinfo/<string:id>', methods=['POST', 'GET'])  # 요청 url 등록
def stationinfo(id):
    res = bus_service.getStationinfo(id)
    return render_template('bus/stationinfo.html', res=res, flag=True)


@bp.route('/addmybus/<string:busid>', methods=['POST', 'GET'])
def addmybus(busid):
    res = bus_service.getBusinfoByBusid(busid)
    id = session['loginid']
    bus = ''
    check = True
    for i in res:
        bus = i
    res2 = bus_service.myBusList(id)
    for i in res2:
        if bus.busid == i.busid:
            check = False
    if check:
        bus_service.addMyBus(
            Bus(id=id, busid=bus.busid, busnm=bus.busnm, ststat=bus.ststat, edstat=bus.edstat, sttime=bus.sttime,
                edtime=bus.edtime, term=bus.term))
        msg = '등록이 완료되었습니다.'
    else:
        msg = '해당 버스는 이미 등록이 되어 있습니다.'
    return render_template('bus/result.html', msg=msg)


@bp.route('/delbus/<string:busid>', methods=['POST', 'GET'])
def delmybus(busid):
    bus_service.delbus(busid)
    msg = '버스 즐겨찾기 삭제가 완료되었습니다.'
    return render_template('bus/result.html', msg=msg)
