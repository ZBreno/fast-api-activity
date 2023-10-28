from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.attendance import AttendanceMemberReq
from typing import List
from cqrs.attendance.command.create_handlers import CreateAttendanceCommandHandler
from cqrs.attendance.command.update_handlers import UpdateAttendanceCommandHandler
from cqrs.attendance.command.delete_handlers import DeleteAttendanceCommandHandler
from cqrs.attendance.commands import AttendanceCommand
from cqrs.attendance.queries import AttendanceListQuery
from cqrs.attendance.query.query_handlers import ListAttendanceQueryHandler

router = APIRouter(prefix='/attendance', tags=['Attendance'])



def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add", response_model=AttendanceMemberReq)
def create_attendance(req: AttendanceMemberReq, sess: Session = Depends(sess_db)):
    
    handler = CreateAttendanceCommandHandler(sess)
    attendance = req.model_dump()
    
    command = AttendanceCommand()
    command.details = attendance
    
    result = handler.handle(command)

    if result:
        return JSONResponse(content=jsonable_encoder(attendance), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create attendance problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/update/{attendance_id}")
def update_attendance(attendance_id: int, req: AttendanceMemberReq, sess: Session = Depends(sess_db)):
    handler = UpdateAttendanceCommandHandler(sess)
    attendance = req.model_dump()
    
    attendance["id"] = attendance_id
    command = AttendanceCommand()
    command.details = attendance
    
    result = handler.handle(command)

    if result:
        return JSONResponse(content={'message': 'attendance updated successfully'}, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'update profile error'}, status_code=500)


@router.delete("/delete/{attendance_id}")
def delete_attendance(attendance_id: int, sess: Session = Depends(sess_db)):
    handler = DeleteAttendanceCommandHandler(sess)
    result = handler.handle(attendance_id)
    if result:
        return JSONResponse(content={'message': 'attendance deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete profile error'}, status_code=500)


@router.get("/list", response_model=List[AttendanceMemberReq])
def list_attendance(sess: Session = Depends(sess_db)):
    handler = ListAttendanceQueryHandler(sess)
    query: AttendanceListQuery = handler.handle_all()

    return JSONResponse(content=jsonable_encoder(query.records), status_code=status.HTTP_200_OK)


@router.get("/attendance/{attendance_id}", response_model=AttendanceMemberReq)
def get_attendance(attendance_id: int, sess: Session = Depends(sess_db)):
    handler = ListAttendanceQueryHandler(sess)
    query: AttendanceListQuery = handler.handle_one(attendance_id=attendance_id)

    return JSONResponse(content=jsonable_encoder(query.records), status_code=status.HTTP_200_OK)
