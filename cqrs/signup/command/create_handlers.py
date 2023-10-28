from cqrs.signup.handlers import ICommandHandler
from repository.sqlalchemy.signup import SignupRepository
from cqrs.signup.commands import SignupCommand
from sqlalchemy.orm import Session
class CreateSignupCommandHandler(ICommandHandler):
    def __init__(self, sess: Session):
        self.repo: SignupRepository = SignupRepository(sess)
    
    def handle(self, command: SignupCommand):
        print(command.details)
        result = self.repo.insert_signup(command.details)
        
        return result