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

- [Página Inicial](telas/FireShot_Capture064-Página_Inicial-127.0.0.1.png)
- [Criar Conta](telas/FireShot Capture 065 - Registrar - 127.0.0.1.png)
- [Solicitar Equipamento](telas/FireShot Capture 066 - Home - 127.0.0.1.png)
- [Cadastrar Ativo](telas/FireShot Capture 067 - Cadastrar Ativo - 127.0.0.1.png)
- [Cadastrar Proprietário](telas/FireShot Capture 068 - Cadastrar Proprietário - 127.0.0.1.png)
- [Estoque](telas/FireShot Capture 070 - Estoque - 127.0.0.1.png)
- [Editar Ativo](telas/FireShot Capture 071 - Edit - Ativo - 127.0.0.1.png)
- [Gerar Transação](telas/FireShot Capture 072 - Adicionar Estoque - 127.0.0.1.png)
- [Proprietários](telas/FireShot Capture 073 - Proprietários - 127.0.0.1.png)
- [Minhas Solicitações](telas/FireShot Capture 074 - Feed - 127.0.0.1.png)
- [Todas Solicitações](telas/FireShot Capture 075 - Solicitações - 127.0.0.1.png)
- [Todas Transações](telas/FireShot Capture 076 - Transações - 127.0.0.1.png)
- [Dashboard](telas/FireShot Capture 077 - Dashboard - 127.0.0.1.png)
- [Dark Mode](telas/FireShot Capture 080 - Home - 127.0.0.1.png)
- [Aumentar Fonte](telas/FireShot Capture 107 - Home - Aumentar Fonte.png)
- [Interface Admin](telas/FireShot Capture 108 - Ativos - Painel de Controle.png)

## Instalação

1. Clone ou baixe este repositório em sua máquina local
2. Acesse o diretório do projeto
3. Instale as dependências necessárias: ```pip install -r requirements.txt```
4. Configure as variáveis de ambiente necessárias, como as credenciais do banco de dados ou outras configurações específicas do seu ambiente.
5. Configura sua chave da API sendgrid,  configure seu sender e defina o email.
6. Inicie o servidor: ```py main.py```
7. Acesse o software pelo seu navegador em [http://127.0.0.1:5000](http://127.0.0.1:5000)
