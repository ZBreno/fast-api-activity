from handlers import ICommandHandler
from repository.sqlalchemy.trainers import TrainersRepository
from command import ProfileTrainerCommand

class DeleteTrainerCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: TrainersRepository = TrainersRepository()
    
    def handle(self, command: ProfileTrainerCommand):
        result = self.repo.delete_trainer(command.details)
        
        return result