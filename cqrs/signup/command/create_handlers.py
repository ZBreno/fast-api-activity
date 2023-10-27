from handlers import ICommandHandler
from repository.sqlalchemy.signup import SignupRepository
from command import SignupCommand

class CreateSignupCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: SignupRepository = SignupRepository()
    
    def handle(self, command: SignupCommand):
        result = self.repo.insert_signup(command.details)
        
        return result