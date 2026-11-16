
from fastapi import FastAPI

from routes.CategoriaEquipamentosRoutes import categoria_equipamento_router
from routes.EquipamentosRoutes import equipamento_router
from routes.PerfilRoutes import perfil_router
from routes.UsuarioRoutes import usuario_router
from routes.AuthRoutes import auth_routes


app = FastAPI(
    title="Primeira API de Wagner",
    description="Primeira API desenvolvida por Wagner",
    version="0.0.1"
)


# Registro das rotas
app.include_router(auth_routes)
app.include_router(categoria_equipamento_router)
app.include_router(equipamento_router)
app.include_router(perfil_router)
app.include_router(usuario_router)


@app.get("/")
def root():
    return {"message": "API funcionando"}


@app.get("/config")
def config():
    return {
        "titulo": "Primeira API de Wagner",
        "versao": "0.0.1"
    }
