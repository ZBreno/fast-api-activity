from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.trainers import ProfileTrainersReq
from domain.data.sqlalchemy_models import Profile_Trainers
from repository.sqlalchemy.trainers import TrainersRepository
from typing import List
from cqrs.trainers.command.create_handlers import CreateTrainerCommandHandler
from cqrs.trainers.command.update_handlers import UpdateTrainerCommandHandler
from cqrs.trainers.command.delete_handlers import DeleteTrainerCommandHandler
from cqrs.trainers.commands import ProfileTrainerCommand
from cqrs.trainers.queries import ProfileTrainerListQuery
from cqrs.trainers.query.query_handlers import ListTrainerQueryHandler
router = APIRouter()


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("trainer/", response_model=ProfileTrainersReq)
def create_trainer(req: ProfileTrainersReq, sess: Session = Depends(sess_db)):
    handler = CreateTrainerCommandHandler(sess)
    trainer = req.model_dump()
    
    command = ProfileTrainerCommand()
    command.details = trainer
    
    result = handler.handle(command)

    if result:
        return JSONResponse(content=jsonable_encoder(trainer), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create trainer problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("trainer/{trainer_id}")
def update_trainer(trainer_id: int, req: ProfileTrainersReq, sess: Session = Depends(sess_db)):
    handler = UpdateTrainerCommandHandler(sess)
    trainers = req.model_dump()
    
    trainers["id"] = trainer_id
    command = ProfileTrainerCommand()
    command.details = trainers
    
    result = handler.handle(command)

    if result:
        return JSONResponse(content={'message': 'trainer updated successfully'}, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'update profile error'}, status_code=500)


@router.delete("trainer/{trainer_id}")
def delete_trainer(trainer_id: int, sess: Session = Depends(sess_db)):
    handler = DeleteTrainerCommandHandler(sess)
    result = handler.handle(trainer_id)

    if result:
        return JSONResponse(content={'message': 'trainer deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete trainer error'}, status_code=500)


@router.get("trainer/", response_model=List[ProfileTrainersReq])
def list_trainer(sess: Session = Depends(sess_db)):
    handler = ListTrainerQueryHandler(sess)
    query: ProfileTrainerListQuery = handler.handle_all()

    return JSONResponse(content=jsonable_encoder(query.records), status_code=status.HTTP_200_OK)


@router.get("trainer/{trainer_id}", response_model=ProfileTrainersReq)
def list_trainer(trainer_id: int, sess: Session = Depends(sess_db)):
    handler = ListTrainerQueryHandler(sess)
    query: ProfileTrainerListQuery = handler.handle_one()

    return JSONResponse(content=jsonable_encoder(query.records), status_code=status.HTTP_200_OK)
