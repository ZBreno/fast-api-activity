from cqrs.trainers.handlers import ICommandHandler
from repository.sqlalchemy.trainers import TrainersRepository

class DeleteTrainerCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: TrainersRepository = TrainersRepository()
    
    def handle(self, trainer_id: int):
        result = self.repo.delete_trainer(trainer_id)
        
        return result