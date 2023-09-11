from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, DateField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Regexp
from aplicacao.models import Usuario, Proprietario, Ativo

class FormLogin(FlaskForm):
    cpf = StringField("CPF", validators=[DataRequired(), Length(11)])
    senha = PasswordField("Senha", validators=[DataRequired()])
    remember = BooleanField("Continuar conectado")
    botao_confirmacao = SubmitField("Entrar")

    def validate_cpf(self, cpf): 
        usuario = Usuario.query.filter_by(cpf=cpf.data).first()
        if not usuario:
            raise ValidationError("Erro! Usuário não existe!")
        
class FormCriarConta(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(max=75)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(11), Regexp(r'^\d{10}(?:\d|X|x)$', message='Erro! CPF inválido')])
    email = StringField("Email", validators=[DataRequired(), Length(max=250), Regexp(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', message="E-mail inválido")])
    senha = PasswordField("Senha", validators=[DataRequired()])
    confirmacao_senha = PasswordField("Confirme sua senha", validators=[DataRequired(), EqualTo("senha", message="Senhas não coincidem!")])
    botao_confirmacao = SubmitField("Registrar")

    def validate_cpf(self, cpf): 
        usuario = Usuario.query.filter_by(cpf=cpf.data).first()
        if usuario:
            raise ValidationError("Erro! CPF já cadastrado, faça login para continuar")
        
    def validate_email(self, email): 
        email = Usuario.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Erro! E-mail já utilizado!")
        
    def validate_senha(self, senha):
        if len(senha.data) < 8:
            raise ValidationError("A senha deve ter mais de 8 caracteres")
        
class FormAtivos(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(max=75)])
    tipo = SelectField("Tipo",validators=[DataRequired()], 
                            choices=[('Software','Software'), 
                                    ('Hardware','Hardware'),
                                    ('Licença','Licença')], default='Software')
    descricao = TextAreaField("Descrição", validators=[DataRequired(), Length(max=500)])
    data_aquisicao = DateField("Data de Aquisição", validators=[DataRequired()])
    data_garantia = DateField("Validade da Garantia", validators=[DataRequired()])
    quantidade_estoque = IntegerField("Quantidade em Estoque", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")

class FormProprietario(FlaskForm):
    nome = StringField("Nome Completo", validators=[DataRequired(), Length(max=75)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(11), Regexp(r'^\d{10}(?:\d|X|x)$', message='Erro! CPF inválido')])
    cargo = StringField("Cargo", validators=[DataRequired(), Length(max=50)])
    departamento = StringField("Departamento", validators=[DataRequired(), Length(max=20)])
    botao_confirmacao = SubmitField("Registrar")

    def validate_departamento(self, departamento):
        departamento.data = departamento.data.capitalize()
        return departamento.data
    
class FormSolicitacao(FlaskForm):
    descricao = TextAreaField("Descrição", validators=[DataRequired(), Length(max=500)])
    quantidade = IntegerField("Quantidade", validators=[DataRequired()])
    ativo = SelectField("Ativo", validators=[DataRequired()], choices=[])
    status = SelectField("Status", validators=[DataRequired()], choices=[('Aguardando', 'Aguardando'), 
                                                                        ('Finalizado', 'Finalizado')], default="Aguardando")
    botao_confirmacao = SubmitField("Gerar Solicitação")

class FormTransacaoEstoque(FlaskForm):
    tipo = SelectField("Tipo", validators=[DataRequired()], choices=[('Entrada','Entrada'), 
                                                                    ('Saída','Saída')], default='Entrada')
    descricao = TextAreaField("Descrição", validators=[DataRequired(), Length(max=500)])
    quantidade = IntegerField("Quantidade", validators=[DataRequired()])
    ativo = SelectField("Ativo", validators=[DataRequired()], choices=[])
    proprietario = SelectField("Destinado ao (a)", validators=[DataRequired()], choices=[])
    botao_confirmacao = SubmitField("Gerar Transação")

    def validate_quantidade(self, quantidade):
        tipo = self.tipo.data
        ativo = Ativo.query.filter_by(id=self.ativo.data).first()

        if tipo == 'Saída' and int(ativo.quantidade_estoque) < int(quantidade.data):
            raise ValidationError("Quantidade solicitado é maior do que disponivel em estoque!")