# Software para gerenciamento de estoque de ativos internos de TI e solicitação de equipamentos.

O projeto a seguir se trata de software para gerenciamento de estoque de ativos internos de TI e solicitação de equipamentos, desenvolvido como parte da disciplina Projeto Integrador II. O objetivo do software é fornecer uma solução eficiente e organizada para o controle e acompanhamento dos ativos internos do setor de informática.

## Índice

<!--ts-->
* [Funcionalidades](#Funcionalidades)
* [Técnologias Utilizadas](#Técnologias-Utilizadas)
* [Screenshots](#Screenshots)
* [Instalação](#Instalação)
<!--te-->

## Funcionalidades

## Técnologias Utilizadas

- Linguagem de Programação: Python, Javascript; <br/>
- Framework: Flask; <br/>
- Banco de Dados: SQLalchemy - SQlite3; <br/>
- API: Sendgrid; <br/>

## Screenshots

- [Página Inicial](telas/Página-Inicial.png)
- [Criar Conta](telas/Registrar.png)
- [Solicitar Equipamento](telas/Home.png)
- [Cadastrar Ativo](telas/Cadastrar-Ativo.png)
- [Cadastrar Proprietário](telas/Cadastrar-Proprietario.png)
- [Estoque](telas/Estoque.png)
- [Editar Ativo](telas/Editar-Ativo.png)
- [Gerar Transação](telas/Gerar-Transação.png)
- [Proprietários](telas/Proprietarios.png)
- [Minhas Solicitações](telas/Minhas-Solicitacoes.png)
- [Todas Solicitações](telas/Todas-Solicitacoes.png)
- [Todas Transações](telas/Todas-Transacoes.png)
- [Dashboard](telas/Dashboard.png)
- [Dark Mode](telas/Dark-Mode.png)
- [Aumentar Fonte](telas/Aumentar-Fonte.png)
- [Interface Admin](telas/Interface-Admin2.png)

## Instalação

1. Clone ou baixe este repositório em sua máquina local
2. Acesse o diretório do projeto
3. Instale as dependências necessárias: ```pip install -r requirements.txt```
4. Configure as variáveis de ambiente necessárias, como as credenciais do banco de dados ou outras configurações específicas do seu ambiente.
5. Configura sua chave da API sendgrid,  configure seu sender e defina o email.
6. Inicie o servidor: ```py main.py```
7. Acesse o software pelo seu navegador em [http://127.0.0.1:5000](http://127.0.0.1:5000)
