from cqrs.login.handlers import IQueryHandler
from cqrs.login.queries import LoginListQuery
from repository.sqlalchemy.login import LoginRepository
from typing import List


class ListLoginQueryHandler(IQueryHandler):
    def __init__(self):
        self.repo: LoginRepository = LoginRepository()
        self.query: LoginListQuery = LoginListQuery()

    def handle_all(self) -> List[LoginListQuery]:
        data = self.repo.get_all_trainers()
        self.query.records = data

        return self.query

    def handle_one(self, trainer_id: int) -> LoginListQuery:
        data = self.repo.get_trainers(trainer_id)

        self.query.records = data

        return self.query
