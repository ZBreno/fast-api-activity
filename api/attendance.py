from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.attendance import AttendanceMemberReq
from domain.data.sqlalchemy_models import Attendance_Member
from repository.sqlalchemy.attendance import AttendanceRepository
from typing import List

router = APIRouter()


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("attendance/", response_model=AttendanceMemberReq)
def create_attendance(req: AttendanceMemberReq, sess: Session = Depends(sess_db)):
    repo: AttendanceRepository = AttendanceRepository(sess)

    attendance = Attendance_Member(id=req.id, member_id=req.member,
                                   timeout=req.timeout, timein=req.timein, date_log=req.date_log)
    result = repo.insert_attendance(attendance)

    if result:
        return JSONResponse(content=attendance, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create attendance problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("attendance/{attendance_id}")
def update_attendance(attendance_id: int, req: AttendanceMemberReq, sess: Session = Depends(sess_db)):
    attendance_dict = req.dict(exclude_unset=True)
    repo: AttendanceRepository = AttendanceRepository(sess)
    result = repo.update_attendance(attendance_id, attendance_dict)

    if result:
        return JSONResponse(content={'message': 'attendance updated successfully'}, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'update profile error'}, status_code=500)


@router.delete("attendance/{attendance_id}")
def delete_attendance(attendance_id: int, sess: Session = Depends(sess_db)):
    repo: AttendanceRepository = AttendanceRepository(sess)
    result = repo.delete_attendance(attendance_id)

    if result:
        return JSONResponse(content={'message': 'attendance deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete profile error'}, status_code=500)


@router.get("attendance/", response_model=List[AttendanceMemberReq])
def list_attendance(sess: Session = Depends(sess_db)):
    repo: AttendanceRepository = AttendanceRepository(sess)
    result = repo.get_all_attendance()
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)


@router.get("attendance/{attendance_id}", response_model=AttendanceMemberReq)
def list_attendance(attendance_id: int, sess: Session = Depends(sess_db)):
    repo: AttendanceRepository = AttendanceRepository(sess)
    result = repo.get_attendance(attendance_id)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
