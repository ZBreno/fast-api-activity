from typing import Dict, Any
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import Profile_Members

class MembersRepository:
    
    def __init__(self, sess: Session):
        self.sess.Session = sess
        
    def insert_member(self, member: Profile_Members):
        try:
            self.sess.add(member)
            self.sess.commit()
        except:
            return False
        return True
    
    def update_member(self, id: int, details: Dict[str, Any]):
        try:
            self.sess.query(Profile_Members).filter(Profile_Members.id == id).update(details)
            self.sess.commit()
        except:
            return False
        return True

    def delete_member(self, id: int) -> bool:
        try:
            member = self.sess.query(Profile_Members).filter(Profile_Members.id == id).delete()
            self.sess.commit()
        except:
            return False
        return True
    
    def get_all_member(self):
        return self.sess.query(Profile_Members).all() 
    
    def get_member(self, id:int): 
        return self.sess.query(Profile_Members).filter(Profile_Members.id == id).one_or_none()
    