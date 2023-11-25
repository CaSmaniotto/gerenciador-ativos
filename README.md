# Software para gerenciamento de estoque de ativos internos de TI e solicitação de equipamentos.

O projeto a seguir se trata de software para gerenciamento de estoque de ativos internos de TI e solicitação de equipamentos, desenvolvido como parte da disciplina Projeto Integrador II. O objetivo do software é fornecer uma solução eficiente e organizada para o controle e acompanhamento dos ativos internos do setor de informática.

## Lembrete
Um usuário comum terá acesso apenas a página de geração de solitação e visualização das mesmas, as demais funcionalidades estão restringidas a usuários com nível de permissão 2.

## Índice

<!--ts-->
* [Funcionalidades](#Funcionalidades)
* [Técnologias Utilizadas](#Técnologias-Utilizadas)
* [Screenshots](#Screenshots)
* [Instalação](#Instalação)
<!--te-->

## Funcionalidades

- Envio de emails: Ações como: solicitar equipamento, finalizar solicitação e criar conta geram envio de emails automaticos.
- Cadastro de usuário: Permite que o usuário crie uma conta fornecendo informações como, por exemplo: nome, cpf, email e senha.
- Cadastro de ativo: Permite que o usuário com permissão possa criar um novo ativo, forcenendo informações como: nome, tipo, descrição, data de  garantia e validade e a quantia inicial em estoque.
- Cadastro de proprietários: Permite ao usuário com permissão cadastrar um novo proprietário, fornecendo: nome, cpf, cargo e departamento.
- Estoque: Permite a visualização dos itens em estoque de forma detalhada e precisa.
- Acessibilidade: Como opções de acessebilidade estão disponíveis: opção de modo escuro (darkmode) e opção para aumento de fonte.
- Solicitar equipamento: Um usuário pode gerar uma solicitação de um ativo, informando: nome do ativo, quantidade e uma descrição (motivo). Após criada, essa solicitação pode ser atendida e finalizada por um administrador.
- Transações: Um usuário com permissão poderá gerar uma transação (entrada ou saída de estoque), fornencendo informações como: tipo (saída ou entrada), descrição, ativo, quantidade e destinatário (proprietário que irá receber o ativo no caso de saída, ou no caso de uma entrada, aquele que irá realizar o reabastecimento.
- Visualização detalhada e gerenciamento: O usuário com permissão pode visualizar de forma detalhada e precisa usuários, proprietários, ativos, transações e solicitações, além de poder realizar ações como editar ou excluir informações.
- Dashboard: O dashboard oferece uma variedade de gráficos e visualizações para representar seus dados de forma clara e eficaz. Desde gráficos de barras a pizza, cada elemento foi projetado para oferecer insights instantâneos.
- Interface Admin: Um painel de controle que proporciona controle total sobre perfis de usuários, permissões e demais informações.

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
