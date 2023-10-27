from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.members import ProfileMembersReq
from domain.data.sqlalchemy_models import Profile_Members
from repository.sqlalchemy.members import MembersRepository
from typing import List

router = APIRouter()


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("member/", response_model=ProfileMembersReq)
def create_member(req: ProfileMembersReq, sess: Session = Depends(sess_db)):
    repo: MembersRepository = MembersRepository(sess)

    member = Profile_Members(id=req.id, firstname=req.firstname,
                             lastname=req.lastname, age=req.age, height=req.height, weight=req.weight, membership_type=req.membership_type, trainer_id=req.trainer_id, login=req.login, attendance=req.attendance, gclass=req.gclass)
    result = repo.insert_member(member)

    if result:
        return JSONResponse(content=member, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create member problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("member/{member_id}")
def update_member(member_id: int, req: ProfileMembersReq, sess: Session = Depends(sess_db)):
    member_dict = req.dict(exclude_unset=True)
    repo: MembersRepository = MembersRepository(sess)
    result = repo.update_member(member_id, member_dict)

    if result:
        return JSONResponse(content={'message': 'member updated successfully'}, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'update profile error'}, status_code=500)


@router.delete("member/{member_id}")
def delete_member(member_id: int, sess: Session = Depends(sess_db)):
    repo: MembersRepository = MembersRepository(sess)
    result = repo.delete_member(member_id)

    if result:
        return JSONResponse(content={'message': 'member deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete member error'}, status_code=500)


@router.get("member/", response_model=List[ProfileMembersReq])
def list_member(sess: Session = Depends(sess_db)):
    repo: MembersRepository = MembersRepository(sess)
    result = repo.get_all_member()
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)


@router.get("member/{member_id}", response_model=ProfileMembersReq)
def list_member(member_id: int, sess: Session = Depends(sess_db)):
    repo: MembersRepository = MembersRepository(sess)
    result = repo.get_member(member_id)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
