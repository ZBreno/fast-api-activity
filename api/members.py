from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.members import ProfileMembersReq
from typing import List
from cqrs.members.command.create_handlers import CreateProfileMemberCommandHandler
from cqrs.members.command.update_handlers import UpdateProfileMemberCommandHandler
from cqrs.members.command.delete_handlers import DeleteProfileMemberCommandHandler
from cqrs.members.commands import ProfileMemberCommand
from cqrs.members.queries import ProfileMembersListQuery
from cqrs.members.query.query_handlers import ListProfileMembersQueryHandler

router = APIRouter(prefix='/members', tags=['Members'])



def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add", response_model=ProfileMembersReq)
def create_member(req: ProfileMembersReq, sess: Session = Depends(sess_db)):
    handler = CreateProfileMemberCommandHandler(sess)
    member = req.model_dump()

    command = ProfileMemberCommand()
    command.details = member

    result = handler.handle(command)

    if result:
        return JSONResponse(content=jsonable_encoder(member), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create member problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/update/{member_id}")
def update_member(member_id: int, req: ProfileMembersReq, sess: Session = Depends(sess_db)):
    handler = UpdateProfileMemberCommandHandler(sess)
    member = req.model_dump()

    member["id"] = member_id
    command = ProfileMemberCommand()
    command.details = member

    result = handler.handle(command)

    if result:
        return JSONResponse(content={'message': 'member updated successfully'}, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'update profile error'}, status_code=500)


@router.delete("/delete/{member_id}")
def delete_member(member_id: int, sess: Session = Depends(sess_db)):
    handler = DeleteProfileMemberCommandHandler(sess)
    result = handler.handle(member_id)

    if result:
        return JSONResponse(content={'message': 'member deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete member error'}, status_code=500)


@router.get("/list", response_model=List[ProfileMembersReq])
def list_member(sess: Session = Depends(sess_db)):
    handler = ListProfileMembersQueryHandler(sess)
    query: ProfileMembersListQuery = handler.handle_all()
    return JSONResponse(content=jsonable_encoder(query.records), status_code=status.HTTP_200_OK)


@router.get("/member/{member_id}", response_model=ProfileMembersReq)
def list_member(member_id: int, sess: Session = Depends(sess_db)):
    handler = ListProfileMembersQueryHandler(sess)
    query: ProfileMembersListQuery = handler.handle_one(member_id)

    return JSONResponse(content=jsonable_encoder(query.records), status_code=status.HTTP_200_OK)
