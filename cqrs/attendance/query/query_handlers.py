from cqrs.attendance.handlers import IQueryHandler
from cqrs.attendance.queries import AttendanceListQuery
from repository.sqlalchemy.attendance import AttendanceRepository
from typing import List
class ListAttendanceQueryHandler(IQueryHandler):
    def __init__(self):
        self.repo: AttendanceRepository = AttendanceRepository()
        self.query: AttendanceListQuery = AttendanceListQuery()
        
    def handle_all(self) -> List[AttendanceListQuery]:
        data = self.repo.get_all_attendance()
        self.query.records = data
        
        return self.query
    
    def handle_one(self, attendance_id: int) -> AttendanceListQuery:
        data = self.repo.get_attendance(attendance_id)
        
        self.query.records = data
        
        return self.query
        
        