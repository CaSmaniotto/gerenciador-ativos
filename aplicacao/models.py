from aplicacao import database, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.filter_by(id=int(id_usuario)).first()

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    cpf = database.Column(database.String(11), nullable=False, unique=True)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    permissao = database.Column(database.Integer, nullable=False, default=0)

    def __repr__(self):
        return (self.nome)

class Proprietario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    cpf = database.Column(database.String(11), nullable=False, unique=True)
    cargo = database.Column(database.String, nullable=False)
    departamento = database.Column(database.String, nullable=False)
    ativos = database.relationship("Ativo", backref="proprietario", lazy=True)

    def __repr__(self):
        return (self.nome)

class Ativo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False, unique=True)
    tipo = database.Column(database.String, nullable=False)
    descricao = database.Column(database.String, nullable=False)
    data_aquisicao = database.Column(database.DateTime, nullable=False)
    data_garantia = database.Column(database.DateTime, nullable=False)
    status = database.Column(database.String, nullable=False)
    id_proprietario = database.Column(database.Integer, database.ForeignKey('proprietario.id'))

    def __repr__(self):
        return '<Ativo {}>'.format(self.id)

    # def __repr__(self):
    #     return (self.nome)