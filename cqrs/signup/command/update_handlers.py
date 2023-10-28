from cqrs.signup.handlers import ICommandHandler
from repository.sqlalchemy.signup import SignupRepository
from cqrs.signup.commands import SignupCommand
from sqlalchemy.orm import Session


class UpdateSignupCommandHandler(ICommandHandler):
    def __init__(self, sess=Session):
        self.repo: SignupRepository = SignupRepository(sess)

    def handle(self, command: SignupCommand):
        result = self.repo.update_signup(command.details["id"], command.details)

        return result
