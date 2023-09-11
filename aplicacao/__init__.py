from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin
# from datetime import timedelta
from sendgrid import SendGridAPIClient

# api key sendgrid
# sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
sg = SendGridAPIClient("YOUR_API_KEY")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///almoxarifado.db"
app.config["SECRET_KEY"] = "a3190c71717b80582c2b580d8bc02528"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "index"
login_manager.session_protected = None
login_manager.login_message = "Por favor faça login para acessar essa página!"
admin = Admin(app, name='Painel de Controle', template_mode='bootstrap4')

login_manager.login_view = 'index'
login_manager.refresh_view = 'index'
# login_manager.needs_refresh_message = (u"Session timedout, please re-login")
# login_manager.needs_refresh_message_category = "info"

# lembrete: isso aqui gera erro, pois limpa a sessão
# @app.before_request
# def before_request():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(minutes=1)

from aplicacao import routes
