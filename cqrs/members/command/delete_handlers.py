from cqrs.members.handlers import ICommandHandler
from repository.sqlalchemy.members import MembersRepository


class DeleteProfileMemberCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: MembersRepository = MembersRepository()

    def handle(self, member_id: int):
        result = self.repo.delete_member(member_id)

        return result
