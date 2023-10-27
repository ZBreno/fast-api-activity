from handlers import ICommandHandler
from repository.sqlalchemy.attendance import AttendanceRepository
from command import AttendanceCommand

class CreateAttendancerCommandHandler(ICommandHandler):
    def __init__(self):
        self.repo: AttendanceRepository = AttendanceRepository()
    
    def handle(self, command: AttendanceCommand):
        result = self.repo.insert_attendance(command.details)
        
        return result