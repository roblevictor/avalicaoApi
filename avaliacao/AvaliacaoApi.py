from fastapi import FastAPI, Request
import datetime
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()



lista = []



class Item(BaseModel):
    nome: str
    data: datetime.datetime
    posicao: int = 0
    tipo: str
    atendido: bool

    
    def __init__(self, **args):
        super().__init__(posicao = 0 if len(lista) == 0 else lista[len(lista) - 1].posicao + 1, **args )

def getCliente(posicao):
    pessoa = None
    for i in lista:
        if i.posicao == posicao:
            pessoa = i 
    return pessoa

def updateAtendimento(inicio):
    for i in range(inicio,len(lista)):
        lista[i].posicao = lista[i].posicao -1
        if lista[i].posicao == 0: 
            lista[i].atendido == True


@app.get('/fila')
def get_lista():
    return [{'nome': x.nome, 'data': x.data, 'posicao': x.posicao} for x in lista]

@app.get('/fila/{id}')
def getPesso(id):
    pessoa = getCliente(int(id))
    if pessoa == None:
        raise HTTPException(
            status_code=404,
            detail="Pessoa/Cliente não encontrado",
            headers={"X-Error": "There goes my error"},
        )
    pessoa2 = {'nome': pessoa.nome, 'data': pessoa.data, 'posicao': pessoa.posicao}
    return pessoa2

@app.post('/fila')
def getAd(dados:Item):
    print(dados)
    if dados.nome != None and len(dados.nome) > 20:
        return 'O campo nome é obrigatório e deve ter no máximo 20 caracteres'
    if dados.tipo not in ['N', 'n', 'P', 'p']:
        return 'Só é permitido 1 caractere (N ou P)'
    lista.append(dados)
    return dados
 
@app.put('/fila')
def updatePosicao():
    updateAtendimento(0)
    return('Atualizado')

@app.delete('/fila/{id}')
def deletePessoa(id):
    pessoa = getCliente(int(id))
    print(pessoa)
    if pessoa == None:
        raise HTTPException(status_code=404, detail='Item not found')
    index = lista.index(pessoa) 
    lista.remove(pessoa)
    updateAtendimento(index)
    return('Usuario deletado')