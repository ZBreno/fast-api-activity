from typing import List
from domain.data.sqlalchemy_models import Attendance_Member

class AttendanceListQuery:
    def __init__(self):
        self._records: List[Attendance_Member] = list()
        
    @property
    def records(self):
        return self._records
    
    @records.setter
    def records(self, records):
        self._records = records