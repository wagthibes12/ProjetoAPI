from fastapi import APIRouter,Depends,status,HTTPException
from entidades.models import Perfil
from sqlmodel import Session    
from dependencies.dependencies import database
from controllers import PerfilController



perfil_router = APIRouter()

@perfil_router.get("/perfis",
                                  response_model=list[Perfil],
                                  status_code=status.HTTP_200_OK)
def listarperfis(db: Session = Depends (database.get_db)):
    try:
        perfis = PerfilController.buscar_todos_os_perfis(db)
        if not perfis:
            return []
        return perfis
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

                    


@perfil_router.post("/perfis", status_code=status.HTTP_201_CREATED,response_model=Perfil)
def inserir_perfil (perfil : Perfil, db: Session = Depends(database.get_db)):
    # inserir_categoria(categoria,db)
    try: 
        perfil_cadastrado = PerfilController.inserir_perfil(perfil, db)
        return perfil_cadastrado
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


@perfil_router.put("/perfis/{perfil_id}", status_code=status.HTTP_200_OK)
def atualizar_perfil(
    perfil_id: int,
    perfil_data: Perfil,
    db: Session = Depends(database.get_db)
):
    try: 
        return PerfilController.atualizar_perfil(db,perfil_id,perfil_data)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException (status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@perfil_router.delete("/perfis/{perfil_id}",status_code=status.HTTP_204_NO_CONTENT)
def deletar_perfil (perfil_id: int, db: Session = Depends(database.get_db)):
    try:
        PerfilController.deletar_perfil(db, perfil_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except KeyError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except KeyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))