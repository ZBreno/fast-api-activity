from cqrs.trainers.handlers import ICommandHandler
from repository.sqlalchemy.trainers import TrainersRepository
from cqrs.trainers.commands import ProfileTrainerCommand


class UpdateTrainerCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: TrainersRepository = TrainersRepository()

    def handle(self, command: ProfileTrainerCommand):
        result = self.repo.update_trainer(command.details["id"], command.details)

        return result
