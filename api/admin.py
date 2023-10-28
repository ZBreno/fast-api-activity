from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.signup import SignupReq
from typing import List
from cqrs.signup.command.create_handlers import CreateSignupCommandHandler
from cqrs.signup.command.update_handlers import UpdateSignupCommandHandler
from cqrs.signup.command.delete_handlers import DeleteSignupCommandHandler
from cqrs.signup.query.query_handlers import ListSignupQueryHandler, SignupListQuery, ListLoginMembersQueryHandler, ListMemberAttendanceQueryHandler
from cqrs.signup.commands import SignupCommand

router = APIRouter(prefix='/signup', tags=['signup'])


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_signup(req: SignupReq, sess: Session = Depends(sess_db)):

    handler = CreateSignupCommandHandler(sess)
    signup = req.model_dump()
    # signup = dict()
    # signup["id"] = req.id
    # signup["password"] = req.password
    # signup["username"] = req.username

    command = SignupCommand()
    command.details = signup

    result = handler.handle(command)
    if result == True:
        return JSONResponse(content=signup, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create signup problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/list", response_model=List[SignupReq])
def list_signup(sess: Session = Depends(sess_db)):
    handler = ListSignupQueryHandler(sess)
    query: SignupListQuery = handler.handle_all()

    return JSONResponse(content=jsonable_encoder(query.records), status_code=status.HTTP_200_OK)


@router.patch("/update")
def update_signup(id: int, req: SignupReq, sess: Session = Depends(sess_db)):
    handler = UpdateSignupCommandHandler(sess)
    signup = req.dict(exclude_unset=True)
    signup["id"] = id
    command = SignupCommand()
    command.details = signup
    result = handler.handle(command)

    if result:
        return JSONResponse(content={'message': 'profile updated successfully'}, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'update profile error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{id}")
def delete_signup(id: int, sess: Session = Depends(sess_db)):
    handler = DeleteSignupCommandHandler(sess)
    result = handler.handle(id)

    if result:
        return JSONResponse(content={'message': 'profile deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete profile error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/list/{id}", response_model=SignupReq)
def get_signup(id: int, sess: Session = Depends(sess_db)):
    handler = ListSignupQueryHandler(sess)
    query: SignupListQuery = handler.handle_one(signup_id=id)

    return JSONResponse(content=jsonable_encoder(query.records), status_code=status.HTTP_200_OK)


@router.get("/login/memberslist")
def get_join_login_members(sess: Session = Depends(sess_db)):

    handler = ListLoginMembersQueryHandler(sess)
    query: SignupListQuery = handler.handle_join_login_members()

    return JSONResponse(content=jsonable_encoder(query.records), status_code=status.HTTP_200_OK)


@router.get("/member/attendance")
def get_join_member_attendance(sess: Session = Depends(sess_db)):
    handler = ListMemberAttendanceQueryHandler(sess)
    query: SignupListQuery = handler.handle_join_members_attendance()

    return JSONResponse(content=jsonable_encoder(query.records), status_code=status.HTTP_200_OK)
