from cqrs.members.handlers import IQueryHandler
from cqrs.members.queries import ProfileMembersListQuery
from repository.sqlalchemy.members import MembersRepository
from typing import List


class ListProfileMembersQueryHandler(IQueryHandler):
    def __init__(self):
        self.repo: MembersRepository = MembersRepository()
        self.query: ProfileMembersListQuery = ProfileMembersListQuery()

    def handle_all(self) -> List[ProfileMembersListQuery]:
        data = self.repo.get_all_member()
        self.query.records = data

        return self.query

    def handle_one(self, member_id: int) -> ProfileMembersListQuery:
        data = self.repo.get_member(member_id)

        self.query.records = data

        return self.query
