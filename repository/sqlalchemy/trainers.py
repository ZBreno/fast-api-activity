from typing import Dict, Any
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import Profile_Trainers

class TrainersRepository:
    
    def __init__(self, sess: Session):
        self.sess.Session = sess
        
    def insert_trainer(self, trainer: Profile_Trainers):
        try:
            self.sess.add(trainer)
            self.sess.commit()
        except:
            return False
        return True
    
    def update_trainer(self, id: int, details: Dict[str, Any]):
        try:
            self.sess.query(Profile_Trainers).filter(Profile_Trainers.id == id).update(details)
            self.sess.commit()
        except:
            return False
        return True

    def delete_trainer(self, id: int) -> bool:
        try:
            trainers = self.sess.query(Profile_Trainers).filter(Profile_Trainers.id == id).delete()
            self.sess.commit()
        except:
            return False
        return True
    
    def get_all_trainers(self):
        return self.sess.query(Profile_Trainers).all() 
    
    def get_trainers(self, id:int): 
        return self.sess.query(Profile_Trainers).filter(Profile_Trainers.id == id).one_or_none()
    