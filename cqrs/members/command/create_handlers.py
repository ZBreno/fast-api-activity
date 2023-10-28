from cqrs.members.handlers import ICommandHandler
from repository.sqlalchemy.members import MembersRepository
from cqrs.members.commands import ProfileMemberCommand


class CreateProfileMemberCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: MembersRepository = MembersRepository()

    def handle(self, command: ProfileMemberCommand):
        result = self.repo.insert_member(command.details)

        return result
