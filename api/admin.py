from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.signup import SignupReq
from domain.data.sqlalchemy_models import Signup
from repository.sqlalchemy.signup import SignupRepository, LoginMemberRepository, MemberAttendanceRepository
from typing import List
from cqrs.signup.command.create_handlers import CreateSignupCommandHandler
from cqrs.signup.command.update_handlers import UpdateTrainerCommandHandler
from cqrs.signup.command.delete_handlers import DeleteTrainerCommandHandler
from cqrs.signup.query.query_handlers import ListSingupQueryHandler, SignupListQuery
from cqrs.signup.commands import SignupCommand

router = APIRouter()


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup/add")
async def add_signup(req: SignupReq):

    handler = CreateSignupCommandHandler()
    signup = req.dict()

    # trainer_profile["id"] = req.id
    # trainer_profile["password"] = req.password
    # trainer_profile["username"] = req.username

    command = SignupCommand()
    command.details = signup

    result = await handler.handle(command)
    if result == True:
        return JSONResponse(content=req, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create signup problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/signup/list", response_model=List[SignupReq])
async def list_signup(sess: Session = Depends(sess_db)):
    handler = ListSingupQueryHandler()
    query: SignupListQuery = await handler.handle()
    
    return JSONResponse(content=query.records, status=status.HTTP_200_OK)


@router.patch("/signup/update")
async def update_signup(id: int, req: SignupReq, sess: Session = Depends(sess_db)):
    handler = UpdateTrainerCommandHandler()
    signup = req.dict(exclude_unset=True)
    command = SignupCommand()
    command.details = signup
    result = await handler.handle()

    if result:
        return JSONResponse(content={'message': 'profile updated successfully'}, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'update profile error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/signup/delete/{id}")
def delete_signup(id: int, sess: Session = Depends(sess_db)):
    repo: SignupRepository = SignupRepository(sess)
    result = repo.delete_signup(id)
    if result:
        return JSONResponse(content={'message': 'profile deleted successfully'}, status_code=201)
    else:
        return JSONResponse(content={'message': 'delete profile error'}, status_code=500)


@router.get("/signup/list/{id}", response_model=SignupReq)
def get_signup(id: int, sess: Session = Depends(sess_db)):
    repo: SignupRepository = SignupRepository(sess)
    result = repo.get_signup(id)
    return result


@router.get("/login/memberslist")
def get_join_login_members(sess: Session = Depends(sess_db)):
    repo: LoginMemberRepository = LoginMemberRepository(sess)
    result = repo.join_login_members()
    return result


@router.get("/member/attendance")
def get_join_member_attendance(sess: Session = Depends(sess_db)):
    repo: MemberAttendanceRepository = MemberAttendanceRepository(sess)
    result = repo.join_member_attendance()
    return result
