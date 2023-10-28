from typing import Dict, Any
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import Attendance_Member

class AttendanceRepository:
    
    def __init__(self, sess: Session):
        self.sess:Session = sess
        
    def insert_attendance(self, attendance: Attendance_Member) -> bool:
        try:
            self.sess.add(attendance)
            self.sess.commit()
        except:
            return False
        return True
    
    def update_attendance(self, id: int, details: Dict[str, Any]) -> bool:
        try:
            self.sess.query(Attendance_Member).filter(Attendance_Member.id == id).update(details)
            self.sess.commit()
        except:
            return False
        return True
    
    def delete_attendance(self, id: int) -> bool:
        try:
            attendance = self.sess.query(Attendance_Member).filter(Attendance_Member.id == id).delete()
            self.sess.commit()
        except:
            return False
        return True
    
    def get_all_attendance(self):
        return self.sess.query(Attendance_Member).all()
    
    def get_attendance(self, id):
        return self.sess.query(Attendance_Member).filter(Attendance_Member.id == id).one_or_one()
    
    def get_all_signup_sorted_desc(self):
        #pesquisar ne
        return self.sess.query(Attendance_Member.id).order_by(desc(Attendance_Member.id)).all()