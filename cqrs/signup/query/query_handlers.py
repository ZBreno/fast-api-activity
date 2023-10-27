from handlers import IQueryHandler
from queries import SignupListQuery
from repository.sqlalchemy.signup import SignupRepository
from typing import List


class ListSingupQueryHandler(IQueryHandler):
    def __init__(self):
        self.repo: SignupRepository = SignupRepository()
        self.query: SignupListQuery = SignupListQuery()

    def handle_all(self) -> List[SignupListQuery]:
        data = self.repo.get_all_trainers()
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
