from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.login import LoginReq
from cqrs.login.command.create_handlers import CreateLoginCommandHandler
from cqrs.login.command.update_handlers import UpdateLoginCommandHandler
from cqrs.login.command.delete_handlers import DeleteLoginCommandHandler
from cqrs.login.commands import LoginCommand
from cqrs.login.queries import LoginListQuery
from cqrs.login.query.query_handlers import ListLoginQueryHandler

router = APIRouter()


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/login/add")
def add_login(req: LoginReq, sess: Session = Depends(sess_db)):
    handler = CreateLoginCommandHandler(sess)
    login = req.model_dump()

    command = LoginCommand()
    command.details = login

    result = handler.handle(command)

    if result == True:
        return JSONResponse(content=jsonable_encoder(login), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create login problem encountered'}, status_code=500)


@router.patch("/login/update")
def update_login(id: int, req: LoginReq, sess: Session = Depends(sess_db)):
    handler = UpdateLoginCommandHandler(sess)
    login = req.model_dump(exclude_unset=True)
    login["id"] = id
    command = LoginCommand()
    command.details = login
    result = handler.handle(command)

    if result:
        return JSONResponse(content={'message': 'login updated successfully'}, status_code=201)
    else:
        return JSONResponse(content={'message': 'update login error'}, status_code=500)


@router.delete("/login/delete/{id}")
def delete_login(id: int, sess: Session = Depends(sess_db)):
    handler = DeleteLoginCommandHandler(sess)
    result = handler.handle(id)
    if result:
        return JSONResponse(content={'message': 'login deleted successfully'}, status_code=204)
    else:
        return JSONResponse(content={'message': 'delete login error'}, status_code=500)


@router.get("/login/list")
def list_login(sess: Session = Depends(sess_db)):
    handler = ListLoginQueryHandler(sess)
    query: LoginListQuery = handler.handle_all()

    return JSONResponse(content=jsonable_encoder(query.records), status_code=status.HTTP_200_OK)


@router.get("/login/get/{id}")
def get_login(id: int, sess: Session = Depends(sess_db)):
    handler = ListLoginQueryHandler(sess)
    query: LoginListQuery = handler.handle_one()

    return JSONResponse(content=jsonable_encoder(query.records), status_code=status.HTTP_200_OK)
