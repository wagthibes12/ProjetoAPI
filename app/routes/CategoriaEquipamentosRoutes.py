
from fastapi import APIRouter, Depends, status, HTTPException
from entidades.models import CategoriaEquipamento
from sqlmodel import Session

from dependencies.dependencies import database
from dependencies.auth import verifica_permissao
from controllers import CategoriaEquipamentosController


categoria_equipamento_router = APIRouter()


@categoria_equipamento_router.get(
    "/categorias",
    response_model=list[CategoriaEquipamento],
    status_code=status.HTTP_200_OK
)
def listarCategorias(
    db: Session = Depends(database.get_db),
    usuario_atual=Depends(
        verifica_permissao("ADMIN", "GESTOR", "DISCENTE")
    )
):
    try:
        categorias = (
            CategoriaEquipamentosController
            .buscar_todas_categoria_equipamento(db)
        )

        return categorias if categorias else []

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@categoria_equipamento_router.post(
    "/categorias",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaEquipamento
)
def inserir(
    categoria: CategoriaEquipamento,
    db: Session = Depends(database.get_db),
    usuario_atual=Depends(verifica_permissao("ADMIN", "GESTOR"))
):
    try:
        return CategoriaEquipamentosController.inserir_categoria(
            categoria,
            db
        )

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


@categoria_equipamento_router.put(
    "/categorias/{categoria_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaEquipamento
)
def AtualizarCategoria(
    categoria_id: int,
    categoria_data: CategoriaEquipamento,
    db: Session = Depends(database.get_db),
    usuario_atual=Depends(verifica_permissao("ADMIN", "GESTOR"))
):
    try:
        return CategoriaEquipamentosController.atualizar_categoria(
            db,
            categoria_id,
            categoria_data
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


@categoria_equipamento_router.delete(
    "/categorias/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def deletar_categoria(
    categoria_id: int,
    db: Session = Depends(database.get_db),
    usuario_atual=Depends(verifica_permissao("ADMIN", "GESTOR"))
):
    try:
        CategoriaEquipamentosController.deletar_categoria(
            db,
            categoria_id
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
