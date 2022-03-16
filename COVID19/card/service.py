from web_hello.member.vo import Member
from web_hello.member.dao_db import MemberDao


class MemberService:
    loginId = ''  # 기본값이 로그인 상태가 아님!

    def __init__(self):
        self.dao = MemberDao()

    # 추가
    def addMember(self, m: Member):
        self.dao.insert(m)

    def getById(self, id: str) -> Member:
        return self.dao.select(id)

    # 삭제
    def delMember(self, id: str):
        self.dao.delete(id)

    # 수정
    def editMember(self, m: Member):
        self.dao.update(m)
