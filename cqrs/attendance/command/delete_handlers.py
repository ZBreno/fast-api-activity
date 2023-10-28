from cqrs.attendance.handlers import ICommandHandler
from repository.sqlalchemy.attendance import AttendanceRepository

class DeleteAttendanceCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: AttendanceRepository = AttendanceRepository()
    
    def handle(self, attendance_id: int):
        result = self.repo.delete_attendance(attendance_id)
        
        return result