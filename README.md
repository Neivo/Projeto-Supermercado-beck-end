# Projeto-Supermercado-beck-end
Sistema de Promoção de Produtos com FastAPI e MySQL Backend desenvolvido em Python com FastAPI para gerenciar supermercados, produtos e promoções. Permite criar, listar e remover itens do banco de dados. Possui rotas para ativar/desativar promoções e realizar compras baseadas nelas. Integrado com MySQL.
# Projeto Supermercado

## Descrição do Projeto

Este projeto consiste em um backend para um sistema de supermercado que gerencia promoções, cadastro de produtos, supermercados e compras. A aplicação utiliza o FastAPI para fornecer APIs que se comunicam com um banco de dados MySQL.

## Pré-requisitos

- Python 3.7 ou superior instalado.
- MySQL Server instalado e configurado.
- Bibliotecas listadas em `requirements.txt` instaladas (use `pip install -r requirements.txt`).

## Configuração do Ambiente

1. Clone este repositório para sua máquina local.
2. Configure um ambiente virtual (opcional, mas recomendado).
3. Instale as dependências usando `pip install -r requirements.txt`.
4. Certifique-se de ter um servidor MySQL em execução e crie um banco de dados chamado `projeto_mercado`.

## Executando a Aplicação

1. Abra o terminal na pasta raiz do projeto.
2. Execute o arquivo `main.py` com o comando `python main.py`.
3. Acesse `http://localhost:8000/docs` para visualizar e testar as APIs.

## Funcionalidades

### Cadastro de Supermercado

- **URL**: `/cadastrar_supermercado`
- **Método**: `POST`
- **Descrição**: Cadastra um novo supermercado.

### Cadastro de Produto

- **URL**: `/cadastrar_produto`
- **Método**: `POST`
- **Descrição**: Cadastra um novo produto.

### Gerenciamento de Promoções

- **URL**: `/nova_promocao`
- **Método**: `POST`
- **Descrição**: Cria uma nova promoção para um produto específico.

### Compras

- **URL**: `/comprar`
- **Método**: `POST`
- **Descrição**: Realiza uma compra dentro do período de promoção.

## Testes

Execute os testes unitários e de integração usando o Pytest: `pytest`.

## Contribuindo

Sinta-se à vontade para contribuir com melhorias, correções de bugs ou novas funcionalidades. Basta fazer um fork deste repositório, fazer as modificações e criar um pull request.

## Autor: Neivo Sander
