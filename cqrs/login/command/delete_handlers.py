from cqrs.login.handlers import ICommandHandler
from repository.sqlalchemy.login import LoginRepository


class DeleteLoginCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: LoginRepository = LoginRepository()
    
    def handle(self, login_id: int):
        result = self.repo.delete_login(login_id)
        
        return result