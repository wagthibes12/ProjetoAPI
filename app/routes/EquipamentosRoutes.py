from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import Session
from dependencies.dependencies import database
from entidades.models import Equipamento
from controllers.EquipamentoController import cadastrar_equipamento

equipamento_router = APIRouter()

@equipamento_router.post("/equipamentos")
def cadastro_equipamento(Equipamento : Equipamento, db:Session = Depends(database.get_db)):
    try: 
        cadastrar_equipamento(Equipamento,db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    

    