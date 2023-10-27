from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.trainers import ProfileTrainersReq
from domain.data.sqlalchemy_models import Profile_Trainers
from repository.sqlalchemy.trainers import TrainersRepository
from typing import List

router = APIRouter()


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("trainer/", response_model=ProfileTrainersReq)
def create_trainer(req: ProfileTrainersReq, sess: Session = Depends(sess_db)):
    repo: TrainersRepository = TrainersRepository(sess)

    trainer = Profile_Trainers(id=req.id, firstname=req.firstname,
                             lastname=req.lastname, age=req.age, height=req.height, weight=req.weight, trainership_type=req.trainership_type, trainer_id=req.trainer_id, login=req.login, attendance=req.attendance, gclass=req.gclass)
    result = repo.insert_trainer(trainer)

    if result:
        return JSONResponse(content=trainer, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create trainer problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("trainer/{trainer_id}")
def update_trainer(trainer_id: int, req: ProfileTrainersReq, sess: Session = Depends(sess_db)):
    trainer_dict = req.dict(exclude_unset=True)
    repo: TrainersRepository = TrainersRepository(sess)
    result = repo.update_trainer(trainer_id, trainer_dict)

    if result:
        return JSONResponse(content={'message': 'trainer updated successfully'}, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'update profile error'}, status_code=500)


@router.delete("trainer/{trainer_id}")
def delete_trainer(trainer_id: int, sess: Session = Depends(sess_db)):
    repo: TrainersRepository = TrainersRepository(sess)
    result = repo.delete_trainer(trainer_id)

    if result:
        return JSONResponse(content={'message': 'trainer deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete trainer error'}, status_code=500)


@router.get("trainer/", response_model=List[ProfileTrainersReq])
def list_trainer(sess: Session = Depends(sess_db)):
    repo: TrainersRepository = TrainersRepository(sess)
    result = repo.get_all_trainer()
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)


@router.get("trainer/{trainer_id}", response_model=ProfileTrainersReq)
def list_trainer(trainer_id: int, sess: Session = Depends(sess_db)):
    repo: TrainersRepository = TrainersRepository(sess)
    result = repo.get_trainer(trainer_id)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
