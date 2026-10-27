from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from entidades.models import Equipamento
from dependencies.dependencies import database
from controllers import EquipamentoController

equipamento_router = APIRouter()


@equipamento_router.get(
    "/equipamentos",
    response_model=list[Equipamento],
    status_code=status.HTTP_200_OK
)
def listar_equipamentos(db: Session = Depends(database.get_db)):
    try:
        equipamentos = EquipamentoController.buscar_todos_equipamentos(db)

        if not equipamentos:
            return []

        return equipamentos

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@equipamento_router.post(
    "/equipamentos",
    status_code=status.HTTP_201_CREATED,
    response_model=Equipamento
)
def inserir_equipamento(
    equipamento: Equipamento,
    db: Session = Depends(database.get_db)
):
    try:
        equipamento_cadastrado = EquipamentoController.cadastrar_equipamento(
            equipamento,
            db
        )
        return equipamento_cadastrado

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@equipamento_router.put(
    "/equipamentos/{equipamento_id}",
    status_code=status.HTTP_200_OK,
    response_model=Equipamento
)
def atualizar_equipamento(
    equipamento_id: int,
    equipamento_data: Equipamento,
    db: Session = Depends(database.get_db)
):
    try:
        return EquipamentoController.atualizar_equipamento(
            db,
            equipamento_id,
            equipamento_data
        )

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@equipamento_router.delete(
    "/equipamentos/{equipamento_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def deletar_equipamento(
    equipamento_id: int,
    db: Session = Depends(database.get_db)
):
    try:
        EquipamentoController.deletar_equipamento(
            db,
            equipamento_id
        )

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )