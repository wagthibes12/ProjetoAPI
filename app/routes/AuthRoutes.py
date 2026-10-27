from fastapi import APIRouter,Depends,status,HTTPException
from sqlmodel import Session 
from entidades.models import UsuarioLogin
from dependencies.dependencies import database
from controllers.AuthController import fazer_login

auth_routes = APIRouter()

@auth_routes.post("/auth/login")
def login(userLogin:UsuarioLogin,db:Session=(Depends(database.get_db))):
    try:
        info_login = fazer_login(db,userLogin.email,userLogin.senha)
        return info_login
    except ValueError as e:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))
    