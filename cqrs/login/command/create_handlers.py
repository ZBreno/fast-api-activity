from cqrs.login.handlers import ICommandHandler
from repository.sqlalchemy.login import LoginRepository
from cqrs.login.commands import LoginCommand

class CreateLoginCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: LoginRepository = LoginRepository()
    
    def handle(self, command: LoginCommand):
        result = self.repo.insert_login(command.details)
        
        return result