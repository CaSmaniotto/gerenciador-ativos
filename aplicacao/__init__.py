from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from sendgrid import SendGridAPIClient

# sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
sg = SendGridAPIClient("API_KEY")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///almoxarifado.db"
app.config["SECRET_KEY"] = "SECRET_KEY"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "index"
login_manager.session_protected = None
login_manager.login_message = "Por favor faça login para acessar essa página!"
admin = Admin(app, name='Painel de Controle', template_mode='bootstrap4', url='/admin', endpoint='first')

login_manager.login_view = 'index'
login_manager.refresh_view = 'index'

from aplicacao import routes