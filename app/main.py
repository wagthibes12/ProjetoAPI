
from fastapi import FastAPI,Depends
#from routes import aluno_routes,ItemCardapio_routes
from entidades.agenda import Agenda
from dependencies.dependencies import Database  
from sqlmodel import Session,select
import random
import datetime 
from routes.CategoriaEquipamentosRoutes import categoria_equipamento_router
from routes.EquipamentosRoutes import equipamento_router
from routes.PerfilRoutes import perfil_router
from config.config import settings


app = FastAPI(
    title= "Primeira API de <Wagner>",
    description="Primeira API desenvolvida por Wagner",
    version= "0.0.1"
)

app.include_router(categoria_equipamento_router)
app.include_router(equipamento_router)
app.include_router(perfil_router)



@app.get("/")
def root (s: Session = Depends(Database.get_db)):
    return "hello world"


@app.get ("/config")
def config():
    return settings



































































# #app.include_router(aluno_routes.aluno_rotas)
# #app.include_router(ItemCardapio_routes.item_cardapio_routes)



# @app.get("/agenda")
# def agenda(contato:Agenda):
#     return {'contato':contato}

# @app.get("/")
# def root():
#     return {"message":"Olá, esta é minha primeira API"}

# @app.get("/valor")
# def valor(valor):
#     return {"item":valor}

# @app.get("/saudacao")
# def saudacao():
#     return "Olá, bem-vindo à nossa primeira API!"

# @app.get("/status")
# def status():
#     return "Servidor Online e Operante"

# @app.get("/api/versao")
# def versao():
#     return "v1.0.0"

# @app.get("/mensagens/geek")
# def geek():
#     return "Sempre parece impossível até que seja feito."

# @app.get("/sobre/autor")
# def autor():
#     return "Autor: Wagner Tibes de Campos"

# @app.get("/mensagens/bom-dia")
# def comprimento():
#     return "Bom dia, excelente semana de estudos!"

# @app.get("/matematica/pi")
# def pi():
#     return "3.14"

# @app.get("/matematica/quadrado-de-oito")
# def calculo():
#     calculo = 8*8
#     return {"message":f"valor de 8 ao quadrado é {calculo}"}

# @app.get("/matematica/area-quadrado")
# def quadrado():
#     quadrado = 15**2 
#     return {"message":f"valor de quadrado de lado 15 é: {quadrado}"}

# @app.get("/matematica/expressao")
# def expressao():
#     expressao = (10 + 5)*2 
#     return {"message":f"o resultado da expressao matematica é: {expressao}"}

# @app.get("/jogos/dados")
# def dados():
#     dados = random.randint(1,6)
#     return {"message":f"O valor do dado caiu: {dados}"}

# @app.get("/jogos/moeda")
# def moeda():
#     moeda = random.choice(["cara","coroa"])
#     return moeda

# @app.get("/jogos/numero-sorte")
# def numero():
#     numero = random.randint(1,100)
#     return numero 

# @app.get("/jogos/senha-aleatoria")
# def senha():
#     senha = random.randint(1000,9999)
#     return senha 

# @app.get("/aleatorio/fruta")
# def fruta():
#     fruta = random.choice(['banana','manga','abacaxi','laranja'])
#     return fruta

# @app.get("/aleatorio/verdadeiro-falso")
# def verdadeiro_falso():
#     verdadeiro_falso = random.choice(['true','false'])
#     return verdadeiro_falso

# #EXERCICIO 2

# @app.get ("/api/calculadora/soma/{numero1}/{numero2}")
# def soma (numero1:int,numero2:int):
#     return {"soma":numero1+numero2}

# @app.get ("/api/geometria/retangulo/{base}/{altura}")
# def area_retangulo(base:int,altura:int):
#     return {"area": base*altura}

# @app.get ("/api/conversores/temperatura/")
# def conversao (celsius:float):
#     fahrenheit = (celsius * 1.8) + 32
#     return {"celsius": celsius, "fahrenheit": fahrenheit}

# @app.get ("/api/escola/media-simples/{nota1}/{nota2}/{nota3}")
# def media (nota1:float, nota2:float ,nota3:float):
#     media_calculada = (nota1+nota2+nota3)/3
#     return {"media": media_calculada}

# @app.get ("/api/financas/juros-simples/{capital}/{taxa_mensal}/{meses}")
# def juros_simples(capital:float, taxa_mensal:float, meses:int):
#     valor_juros = (capital*taxa_mensal*meses)
#     return {"valor_juros": valor_juros}

# @app.get ("/api/saude/imc/{peso_kg}/{altura_m}")
# def imc (peso_kg:float, altura_m:float):
#     resultado_imc = peso_kg / (altura_m * altura_m)
#     return {"resultado_imc": resultado_imc}

# @app.get ("/api/conversores/tempo-horas")
# def tempo_horas (minutos_totais:int):
#     horas = minutos_totais // 60
#     minutos = minutos_totais % 60
#     return {
#         "minutos_totais": minutos_totais,
#         "horas": horas,}
 
# #@app.get ("/api/loja/aplicar-desconto")
# #def aplicar_desconto (valor_produto:float, porcentagem_desconto)