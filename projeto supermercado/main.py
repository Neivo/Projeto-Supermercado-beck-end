import time
import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

conexao = mysql.connector.connect(
    host='localhost', 
    user='root', 
    password='', 
    database='projeto_mercado'
)

sql = conexao.cursor()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

class Mercado(BaseModel):
    nome: str
    endereco: str

class Produto(BaseModel):
    nome: str
    descricao: str
    imagem_url: str
    preco: float

class Promocao(BaseModel):
    produto_id: int
    data_inicio: int
    data_fim: int
    limite_cpf: int

class Promo(BaseModel):
    promo_id: int
    mercado_id: int

class Comprar(BaseModel):
    mercado_id: int
    produto_id: int
    cpf: int

class Deletar(BaseModel):
    id: int

# MERCADO 
@app.post("/cadastrar_supermercado")
async def cadastrar_supermercado(e: Mercado):
    sql.execute(f"select * from mercado where nome='{e.nome}' and endereco='{e.endereco}'")

    if sql.fetchall():
        return {'data': 'Supermercado já cadastrado'}
    
    sql.execute(f"insert into mercado (nome, endereco) values ('{e.nome}','{e.endereco}')")
    conexao.commit()

    return {'data': 'Mercado cadastrado'}

@app.post("/deletar_supermercado")
async def deletar_supermercado(e:Deletar):
    sql.execute(f"select * from mercado where id='{e.id}'")

    if sql.fetchall():
        sql.execute(f"delete from mercado where id={e.id}")
        return {"data": "Supermercado excluido com sucesso"}
    
    conexao.commit()
    return {"data": "Mercado inexistente"}


# PRODUTO 
@app.post("/cadastrar_produto")
async def cadastrar_produto(e: Produto):
    sql.execute(f"select * from produtos where nome='{e.nome}'")

    if sql.fetchall():
        return {'data': 'Produto já cadastrado'}
    
    sql.execute(f"insert into produtos (nome, descricao, preco, imagem_url) values ('{e.nome}','{e.descricao}', '{e.preco}', '{e.imagem_url}')")
    conexao.commit()

    return {'data': 'Produto cadastrado'}

@app.post("/deletar_produto")
async def deletar_produto(e:Deletar):
    sql.execute(f"select * from produtos where id='{e.id}'")

    if sql.fetchall():
        sql.execute(f"delete from produtos where id={e.id}")
        sql.execute(f"delete from promocao where produto_id='{e.id}'")
        return {"data": "Produto deletado com sucesso"}
    
    conexao.commit()
    return {"data": "Produto inexistente"}


# PROMOCAO 
@app.post("/nova_promocao")
async def nova_promocao(e: Promocao):
    sql.execute(f"select * from produtos where id='{e.produto_id}'")

    if sql.fetchall():
        sql.execute(f"select * from promocao where produto_id='{e.produto_id}'")
        res = sql.fetchall()

        if res:

            return {'data': f'Promoção já existe para esse produto {res}'}
        
        sql.execute(f"insert into promocao (produto_id, data_inicio, data_fim, limite_cliente) values ('{e.produto_id}', '{e.data_inicio}', '{e.data_fim}', '{e.limite_cpf}')")
        return {'data': 'Promoção criada com êxito!'}
    
    conexao.commit()
    return {'data': 'Produto inexistente'}


@app.post("/deletar_promocao")
async def deletar_promocao(e:Deletar):
    sql.execute(f"select * from promocao where id='{e.id}'")

    if sql.fetchall():
        sql.execute(f"delete from promocao where id='{e.id}'")
        return {"data": "Promocao Deletada"}
    
    conexao.commit()
    return {"data": "Promocao de produto não existe"}
    

@app.post("/ativar_promocao")
async def ativar_promocao(e:Promo):
    sql.execute(f"select * from promocao where id='{e.promo_id}'")
    
    if sql.fetchall():
        sql.execute(f"select * from mercado where id='{e.mercado_id}'")
  
        if sql.fetchall():
            sql.execute(f"select * from mercado_promocao where mercado_id='{e.mercado_id}' and promocao_id='{e.promo_id}'")

            if sql.fetchall():
                return {"data": "Promoção ja existe nesse mercado"}
            
            sql.execute(f"insert into mercado_promocao (mercado_id, promocao_id) values ('{e.mercado_id}', '{e.promo_id}')")
            
            return {"data": "Promoção ativada com sucesso!"} 
        
        return {"data": "Não foi possivel encontrar esse mercado"}
    
    conexao.commit()
    return {"data": "Essa promoção não existe"}


@app.post("/desativar_promocao")
async def desativar_promocao(e:Promo):
    sql.execute(f"select * from mercado_promocao where promocao_id='{e.promo_id}' and mercado_id='{e.mercado_id}'")

    if sql.fetchall():
        sql.execute(f"delete from mercado_promocao where promocao_id='{e.promo_id}' and mercado_id='{e.mercado_id}'")
        return {"data": "Promoção encerrada com sucesso"} 
    
    conexao.commit();
    return {"data": "Promoção não encontrada nesse mercado"}
 

@app.post("/comprar")
async def comprar(e:Comprar):
    sql.execute(f"select * from mercado_promocao where mercado_id='{e.mercado_id}'")
    res = sql.fetchall()

    if res:
        resid = res[0][2] 

    if(len(res) > 0):
        
        sql.execute(f"select * from promocao where produto_id='{e.produto_id}' and id='{resid}'")
        res = sql.fetchall()

        if res:
            data_ini = res[0][2]
            data_fim = res[0][3]
            limite_compras = res[0][4]
            hoje = round(time.time() * 1000)

            if (hoje >= int(data_ini)) & (hoje <= int(data_fim)):
                sql.execute(f"select * from compras where id_promocao='{resid}' and cpf='{e.cpf}'")
                res = sql.fetchall()
                if len(res) > limite_compras - 1:
                    lim = len(res)
                    return {"data": f"Limite máximo atingido por CPF {lim}"}
                
                sql.execute(f"insert into compras (id_promocao, cpf) values ('{resid}', '{e.cpf}')")

                return {"data": "Valid time promo"} 
            
            return {"data":f'Tempo de promoção ja acabou {data_ini} {data_fim} {hoje}'}
        
        return {"data": f'Produto não está na promoção'}

    conexao.commit()    
    return {"data": "Promoção nao encontrada para esse produto no mercado atual"}