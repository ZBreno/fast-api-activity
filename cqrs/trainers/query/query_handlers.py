from cqrs.trainers.handlers import IQueryHandler
from cqrs.trainers.queries import ProfileTrainerListQuery
from repository.sqlalchemy.trainers import TrainersRepository
from typing import List

class ListTrainerQueryHandler(IQueryHandler):
    def __init__(self):
        self.repo: TrainersRepository = TrainersRepository()
        self.query: ProfileTrainerListQuery = ProfileTrainerListQuery()
        
    def handle_all(self) -> List[ProfileTrainerListQuery]:
        data = self.repo.get_all_trainers()
        self.query.records = data
        
        return self.query
    
    def handle_one(self, trainer_id: int) -> ProfileTrainerListQuery:
        data = self.repo.get_trainers(trainer_id)
        
        self.query.records = data
        
        return self.query
        
        