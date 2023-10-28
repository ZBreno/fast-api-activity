from cqrs.signup.queries import SignupListQuery, LoginMemberListQuery, MemberAttendanceListQuery
from repository.sqlalchemy.signup import SignupRepository, MemberAttendanceRepository, LoginMemberRepository
from typing import List
from cqrs.signup.handlers import IQueryHandler
from sqlalchemy.orm import Session


class ListSignupQueryHandler(IQueryHandler):
    def __init__(self, sess=Session):
        self.repo: SignupRepository = SignupRepository(sess)
        self.query: SignupListQuery = SignupListQuery()

    def handle_all(self) -> List[SignupListQuery]:
        data = self.repo.get_all_signup()
        self.query.records = data

        return self.query

    def handle_one(self, signup_id: int) -> SignupListQuery:
        data = self.repo.get_signup(signup_id)

        self.query.records = data

        return self.query

    def handle_all_signup_where(self, username: str) -> SignupListQuery:
        data = self.repo.get_all_signup_where(username)

        self.query.records = data

        return self.query

    def handle_all_signup_sorted_desc(self) -> List[SignupListQuery]:
        data = self.repo.get_all_signup_sorted_desc()

        self.query.records = data

        return self.query


class ListLoginMembersQueryHandler(IQueryHandler):
    def __init__(self, sess: Session):
        self.repo: LoginMemberRepository = LoginMemberRepository(sess)
        self.query: LoginMemberListQuery = LoginMemberListQuery()

    def handle_join_login_members(self) -> List[SignupListQuery]:
        data = self.repo.join_login_members()

        self.query.records = data

        return self.query


class ListMemberAttendanceQueryHandler(IQueryHandler):
    def __init__(self, sess: Session):
        self.repo: MemberAttendanceRepository = MemberAttendanceRepository(
            sess)
        self.query: MemberAttendanceListQuery = MemberAttendanceListQuery()

    def handle_join_members_attendance(self) -> List[SignupListQuery]:
        data = self.repo_member.join_member_attendance()

        self.query.records = data

        return self.query

    def handle_outer_join_member(self) -> List[SignupListQuery]:
        data = self.repo_member.outer_join_member()

        self.query.records = data

        return self.query
