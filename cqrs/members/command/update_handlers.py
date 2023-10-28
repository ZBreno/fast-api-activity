from cqrs.members.handlers import ICommandHandler
from repository.sqlalchemy.members import MembersRepository
from commands import ProfileMemberCommand


class UpdateProfileMemberCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: MembersRepository = MembersRepository()

    def handle(self, command: ProfileMemberCommand):
        result = self.repo.update_member(command.details["id"], command.details)

        return result
