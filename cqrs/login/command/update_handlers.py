from cqrs.login.handlers import ICommandHandler
from repository.sqlalchemy.login import LoginRepository
from cqrs.login.commands import LoginCommand

class UpdateLoginCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: LoginRepository = LoginRepository()
    
    def handle(self, command: LoginCommand):
        result = self.repo.update_login(command.details["id"],command.details)
        
        return result