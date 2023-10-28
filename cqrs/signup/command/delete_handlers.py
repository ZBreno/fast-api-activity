from cqrs.signup.handlers import ICommandHandler
from repository.sqlalchemy.signup import SignupRepository
from sqlalchemy.orm import Session

class DeleteSignupCommandHandler(ICommandHandler):
    def __init__(self, sess: Session):
        self.repo: SignupRepository = SignupRepository(sess)
    
    def handle(self, signup_id: int):
        result = self.repo.delete_signup(signup_id)
        
        return result