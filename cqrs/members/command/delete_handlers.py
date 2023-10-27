from handlers import ICommandHandler
from repository.sqlalchemy.members import MembersRepository
from command import ProfileMemberCommand

class DeleteProfileMemberCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: MembersRepository = MembersRepository()
    
    def handle(self, command: ProfileMemberCommand):
        result = self.repo.delete_attendance(command.details)
        
        return result