from cqrs.attendance.handlers import ICommandHandler
from repository.sqlalchemy.attendance import AttendanceRepository
from cqrs.attendance.commands import AttendanceCommand

class UpdateAttendanceCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: AttendanceRepository = AttendanceRepository()
    
    def handle(self, command: AttendanceCommand):
        result = self.repo.update_attendance(command.details["id"], command.details)
        
        return result