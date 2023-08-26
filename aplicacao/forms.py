from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, DateField, TextAreaField
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
    nome = StringField("Nome", validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Regexp(r'^\d{10}(?:\d|X|x)$', message='Erro! CPF inválido')])
    email = StringField("Email", validators=[DataRequired(), Regexp(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', message="E-mail inválido")])
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
        
class FormAtivos(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    tipo = SelectField("Tipo",validators=[DataRequired()], 
                            choices=[('Software','Software'), 
                                    ('Hardware','Hardware'),
                                    ('Licença','Licença')], default='Software')
    descricao = TextAreaField("Descrição", validators=[DataRequired()])
    data_aquisicao = DateField("Data de Aquisição", validators=[DataRequired()])
    data_garantia = DateField("Validade da Garantia", validators=[DataRequired()])
    status = SelectField("Status",validators=[DataRequired()], 
                            choices=[('Em uso','Em uso'), 
                                    ('Em manutenção','Em manutenção'),
                                    ('Descartado','Descartado')], default='Em uso')
    

    proprietario = SelectField("Proprietário", validators=[DataRequired()], choices=[])
    botao_confirmacao = SubmitField("Enviar")

class FormProprietario(FlaskForm):
    nome = StringField("Nome Completo", validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Regexp(r'^\d{10}(?:\d|X|x)$', message='Erro! CPF inválido')])
    cargo = StringField("Cargo", validators=[DataRequired()])
    departamento = StringField("Departamento", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Registrar")