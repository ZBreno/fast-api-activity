from handlers import ICommandHandler
from repository.sqlalchemy.trainers import TrainersRepository
from command import ProfileTrainerCommand

class CreateTrainerCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: TrainersRepository = TrainersRepository()
    
    def handle(self, command: ProfileTrainerCommand):
        result = self.repo.insert_trainer(command.details)
        
        return result