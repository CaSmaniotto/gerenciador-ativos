from aplicacao import database, login_manager, database, admin #manager
from flask_login import UserMixin, current_user
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask import abort

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.filter_by(id=int(id_usuario)).first()

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    cpf = database.Column(database.String(11), nullable=False, unique=True)
    nome = database.Column(database.String(75), nullable=False)
    email = database.Column(database.String(250), nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    permissao = database.Column(database.Integer, nullable=False, default=1)
    solicitacoes = database.relationship("Solicitacao", backref="usuario", lazy=True)

    def __repr__(self):
        return (self.nome)

class Proprietario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(75), nullable=False)
    cpf = database.Column(database.String(11), nullable=False, unique=True)
    cargo = database.Column(database.String(50), nullable=False)
    departamento = database.Column(database.String(20), nullable=False)
    transacoes = database.relationship("TransacaoEstoque", backref="proprietario", lazy=True)

    def __repr__(self):
        return (self.nome)

class Ativo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(75), nullable=False, unique=True)
    tipo = database.Column(database.String, nullable=False)
    descricao = database.Column(database.String(500), nullable=False)
    data_aquisicao = database.Column(database.DateTime, nullable=False)
    data_garantia = database.Column(database.DateTime, nullable=False)
    quantidade_estoque = database.Column(database.Integer, nullable=False)
    solicitacoes = database.relationship("Solicitacao", backref="ativo", lazy=True)
    transacoes = database.relationship("TransacaoEstoque", backref="ativo", lazy=True)

    def __repr__(self):
        return (self.nome)

class Solicitacao(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    descricao = database.Column(database.String(500), nullable=False)
    data = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id')) # quem está gerando
    id_ativo = database.Column(database.Integer, database.ForeignKey('ativo.id'))
    quantidade = database.Column(database.Integer, nullable=False)
    status = database.Column(database.String, nullable=False)

    def __repr__(self):
        return (str(self.id))

class TransacaoEstoque(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    tipo = database.Column(database.String, nullable=False) # entrada ou saíde de estoque
    descricao = database.Column(database.String(500), nullable=False)
    id_ativo = database.Column(database.Integer, database.ForeignKey('ativo.id'))
    quantidade = database.Column(database.Integer, nullable=False)
    id_proprietario = database.Column(database.Integer, database.ForeignKey('proprietario.id')) # para quem está indo ou para estoque
    data = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return (str(self.id))

# modelos interface admin
class ControlUsuario(ModelView):

    def is_accessible(self):
        if current_user.permissao == 2:
            return current_user.is_authenticated
        else:
            return abort(403)
        
    def not_auth(self):
        return "acess denied!"

    form_choices = {
        'permissao': [ (1,"Usuário"), 
                    (2, "Admin")]
    }
    column_list = ['nome', 'cpf', 'email', 'solicitacoes']
    column_filters = ['cpf', 'email', 'solicitacoes']
    form_excluded_columns = ['solicitacoes', 'senha']
    create_modal = True
    edit_modal = True
    can_view_details = True
    can_create = True

class ControlProprietario(ModelView):

    def is_accessible(self):
        if current_user.permissao == 2:
            return current_user.is_authenticated
        else:
            return abort(403)
        
    def not_auth(self):
        return "acess denied!"
    
    column_list = ['nome', 'cpf', 'cargo', 'departamento', 'transacoes']
    column_filters = ['cpf', 'cargo', 'departamento', 'transacoes']
    form_excluded_columns = ['transacoes']
    create_modal = True
    edit_modal = True
    can_view_details = True
    can_create = True

class ControlAtivo(ModelView):

    def is_accessible(self):
        if current_user.permissao == 2:
            return current_user.is_authenticated
        else:
            return abort(403)
        
    def not_auth(self):
        return "acess denied"

    form_choices = {
        'tipo': [ ('Software','Software'), 
                    ('Hardware','Hardware'),
                    ('Licença','Licença')]
    }
    form_excluded_columns = ['transacoes', 'solicitacoes']
    column_list = ['nome', 'tipo', 'descricao', 'data_aquisicao', 'data_garantia', 'quantidade_estoque', 'solicitacoes']
    column_filters = ['data_aquisicao', 'tipo', 'nome', 'quantidade_estoque']
    create_modal = True
    edit_modal = True
    can_view_details = True
    can_create = True

class ControlSolicitacao(ModelView):

    def is_accessible(self):
        if current_user.permissao == 2:
            return current_user.is_authenticated
        else:
            return abort(403)
        
    def not_auth(self):
        return "acess denied"


    form_choices = {
        'status': [ ('Aguardando','Aguardando'), 
                    ('Finalizado','Finalizado')]
    }
    column_filters = ['data', 'usuario', 'status', 'ativo', 'quantidade']
    create_modal = True
    edit_modal = True
    can_view_details = True
    can_create = True

class ControlTransacaoEstoque(ModelView):

    def is_accessible(self):
        if current_user.permissao == 2:
            return current_user.is_authenticated
        else:
            return abort(403)
        
    def not_auth(self):
        return "acess denied"

    form_choices = {
        'tipo': [ ('Entrada','Entrada'), 
                    ('Saída','Saída')]
    }
    column_filters = ['tipo', 'data', 'proprietario', 'ativo']
    create_modal = True
    edit_modal = True
    can_view_details = True
    can_create = True

#interface admin views
admin.add_view(ControlAtivo(Ativo, database.session, name='Ativos'))
admin.add_view(ControlProprietario(Proprietario, database.session, name='Proprietarios'))
admin.add_view(ControlUsuario(Usuario, database.session, name='Usuarios'))
admin.add_view(ControlSolicitacao(Solicitacao, database.session, name='Solicitacoes'))
admin.add_view(ControlTransacaoEstoque(TransacaoEstoque, database.session, name='TransacoesEstoque'))
admin.add_link(MenuLink(name='Voltar', url='/feed'))
admin.add_link(MenuLink(name='Sair', url='/logout'))