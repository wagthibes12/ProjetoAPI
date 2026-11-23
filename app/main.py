
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.CategoriaEquipamentosRoutes import categoria_equipamento_router
from routes.EquipamentosRoutes import equipamento_router
from routes.PerfilRoutes import perfil_router
from routes.UsuarioRoutes import usuario_router
from routes.AuthRoutes import auth_routes
from routes import SolicitacaoRoutes
from routes.EmprestimoRoutes import router as emprestimo_router
from routes.DevolucaoRoutes import router as devolucao_router

from dependencies.dependencies import database


# =========================
# CICLO DE VIDA DA API
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        database.close()


# =========================
# CRIAÇÃO DA API
# =========================

app = FastAPI(
    title="Primeira API de Wagner",
    description="Primeira API desenvolvida por Wagner",
    version="0.0.1",
    lifespan=lifespan
)


# =========================
# CONFIGURAÇÃO CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# REGISTRO DAS ROTAS
# =========================

app.include_router(auth_routes)
app.include_router(categoria_equipamento_router)
app.include_router(equipamento_router)
app.include_router(perfil_router)
app.include_router(usuario_router)
app.include_router(SolicitacaoRoutes.router)
app.include_router(emprestimo_router)
app.include_router(devolucao_router)


# =========================
# ROTA PRINCIPAL
# =========================

@app.get("/")
def root():
    return {
        "message": "API funcionando"
    }


# =========================
# CONFIGURAÇÕES DA API
# =========================

@app.get("/config")
def config():
    return {
        "titulo": "Primeira API de Wagner",
        "versao": "0.0.1"
    }
