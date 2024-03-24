from flask import render_template, url_for, redirect, flash, session, abort
from aplicacao import app, database, bcrypt
from aplicacao.models import Usuario, Ativo, Proprietario, TransacaoEstoque, Solicitacao
from flask_login import login_required, login_user, logout_user, current_user
from aplicacao.forms import FormLogin, FormCriarConta, FormAtivos, FormProprietario, FormTransacaoEstoque, FormSolicitacao
from aplicacao.utils import sendgrid_mail
from collections import defaultdict

@app.errorhandler(403)
def access_denied(e):
    return redirect(url_for('home'))

@app.route("/", methods=["GET", "POST"])
def index():
    form = FormLogin()

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(cpf=form.cpf.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, remember=form.remember.data)
            flash("Logado com sucesso")
            session['usuario'] = usuario.id
            return redirect(url_for("home")) # id_usuario=usuario.id
        else:
            flash("Senha incorreta")
            return redirect("/")
        
    return render_template("index.html", form=form)

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    form = FormCriarConta()

    if form.validate_on_submit():
        hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(
                    cpf=form.cpf.data,
                    nome=form.nome.data,
                    email=form.email.data,
                    senha=hash)
        
        database.session.add(usuario)
        database.session.commit()
        flash("Usuário registrado com sucesso!")

        titulo = "Conta criada com sucesso!"
        mensagem = f"""
        <p>Olá {form.nome.data}, sua conta foi criada com sucesso!<p>
        <br> Caso não tenha sido você, entre em contato conosco respondendo a este email!
        """

        sendgrid_mail(form.email.data, titulo, mensagem)

        return redirect('/')

    return render_template("registrar.html", form=form)

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():

    form = FormSolicitacao()

    ativos = Ativo.query.all()
    form.ativo.choices = [(int(atv.id), atv.nome) for atv in ativos]

    if form.validate_on_submit():
        solicitacao = Solicitacao(descricao=form.descricao.data,
                                    id_usuario=current_user.id,
                                    id_ativo=form.ativo.data,
                                    quantidade=form.quantidade.data,
                                    status='Aguardando')

        database.session.add(solicitacao)
        database.session.commit()

        titulo = "Solicitação Gerada!"
        mensagem = f"""
        <p>Solicitação gerada com sucesso</p>
        <p>Número: {solicitacao.id}</p>
        <p>Solicitante: {current_user.nome}</p>
        <p>Status: {solicitacao.status}</p>
        """

        sendgrid_mail(current_user.email, titulo, mensagem)

        return redirect(url_for("feed"))

    return render_template("home.html", form=form)

@app.route("/ativo", methods=["GET", "POST"])
@login_required
def ativo():
    if current_user.permissao < 2:
        return abort(403)
    form = FormAtivos()

    if form.validate_on_submit():
        ativo = Ativo.query.filter_by(nome=form.nome.data).first()

        if form.data_garantia.data < form.data_aquisicao.data:
            flash("Data de aquisição inferior a de garantia!")
            return redirect("/ativo")
        elif ativo:
            flash("Nome de ativo já utilizado!")
            return redirect("/ativo")
        else:
            ativo = Ativo(nome=form.nome.data,
                        tipo=form.tipo.data,
                        descricao=form.descricao.data,
                        data_aquisicao=form.data_aquisicao.data,
                        data_garantia=form.data_garantia.data,
                        quantidade_estoque=form.quantidade_estoque.data)
            database.session.add(ativo)
            database.session.commit()
            flash("ativo criado com sucesso!")
            return redirect('/estoque')

    return render_template("cadastrar_ativo.html", form=form)

@app.route("/proprietario", methods=["GET", "POST"])
@login_required
def proprietario():
    if current_user.permissao < 2:
        return abort(403)
    form = FormProprietario()

    if form.validate_on_submit():
        proprietario = Proprietario.query.filter_by(cpf=form.cpf.data).first()
        if proprietario:
            flash("Erro! Proprietário já cadastrado!")
            return redirect("/proprietario")
        else:
            proprietario = Proprietario(nome=form.nome.data,
                                        cpf=form.cpf.data,
                                        cargo=form.cargo.data,
                                        departamento=form.departamento.data.lower())
            database.session.add(proprietario)
            database.session.commit()
            flash("Proprietário cadastrado!")
            return redirect('/proprietarios')
    return render_template("cadastrar_proprietario.html", form=form)

@app.route("/feed")
@login_required
def feed():
    solicitacoes = Solicitacao.query.filter_by(id_usuario=current_user.id).order_by(Solicitacao.data.desc()).all()
    return render_template("feed.html", solicitacoes=solicitacoes)

@app.route("/proprietarios")
@login_required
def proprietarios():
    if current_user.permissao < 2:
        return abort(403)
    
    proprietarios = Proprietario.query.all()
    return render_template("proprietarios.html", proprietarios=proprietarios)

item_actions = {
    "ativo": {
        "edit": "edit_ativo",
        "delete": "delete_ativo",
    },
    "proprietario": {
        "edit": "edit_proprietario",
        "delete": "delete_proprietario",
    },
    "solicitacao": {
        "finish": "finish_solicitacao",
    },
}

@app.route("/finish_solicitacao")
@login_required
def finish_solicitacao():
    solicitacao = Solicitacao.query.filter_by(id=session["item_id"]).first()
    if solicitacao.status == "Finalizado":
        return redirect(url_for("solicitacoes"))

    solicitacao.status = "Finalizado"
    database.session.commit()

    titulo = "Solicitação Finalizada"
    mensagem = f"""
    <p>Solicitante: {solicitacao.usuario.nome}</p>
    <p>Número: {solicitacao.id}</p>
    <p>Status: {solicitacao.status}</p>
    """

    sendgrid_mail(solicitacao.usuario.email, titulo, mensagem)

    return redirect(url_for("solicitacoes"))

@app.route("/get_item/<string:item_type>/<string:action>/<int:item_id>")
@login_required
def get_item(item_type, action, item_id):
    if current_user.permissao < 2:
        return abort(403)

    session["item_id"] = item_id

    if item_type in item_actions:
        if action in item_actions[item_type]:
            return redirect(url_for(item_actions[item_type][action]))
    else:
        return redirect("estoque")

@app.route("/estoque/edit_ativo", methods=["GET", "POST"])
@login_required
def edit_ativo():
    if current_user.permissao < 2:
        return abort(403)
    
    ativo_id = session.get('item_id')
    ativo = Ativo.query.get(int(ativo_id))

    form_edit = FormAtivos(obj=ativo)

    if form_edit.validate_on_submit():
        form_edit.populate_obj(ativo)

        database.session.commit()
        flash("Editado com sucesso!")
        return redirect('/estoque')
    return render_template("edit_ativo.html", form=form_edit) 

@app.route("/delete_ativo")
@login_required
def delete_ativo():
    if current_user.permissao < 2:
        return abort(403)
    
    ativo = Ativo.query.get(session.get('item_id'))
    
    database.session.delete(ativo)
    database.session.commit()
    flash("Ativo excluido com sucesso!")

    return redirect(url_for("feed"))

@app.route("/proprietarios/edit_proprietario", methods=["GET", "POST"])
@login_required
def edit_proprietario():
    if current_user.permissao < 2:
        return abort(403)
    
    proprietario_id = session.get('item_id')
    proprietario = Proprietario.query.get(int(proprietario_id))

    form_edit = FormProprietario(obj=proprietario)

    if form_edit.validate_on_submit():
        cpf_existe = Proprietario.query.filter_by(cpf=form_edit.cpf.data).first()
        cpf_atual = Proprietario.query.filter_by(id=session.get('item_id')).first()

        if not cpf_existe or (cpf_existe.cpf == cpf_atual.cpf):
            form_edit.populate_obj(proprietario)

            database.session.commit()
            flash("Editado com sucesso!")
            return redirect('/proprietarios')
        else:
            flash("CPF já utilizado!")

    return render_template("edit_proprietario.html", form=form_edit)

@app.route("/delete_proprietario")
@login_required
def delete_proprietario():
    if current_user.permissao < 2:
        return abort(403)
    
    proprietario = Proprietario.query.get(session.get('item_id'))

    database.session.delete(proprietario)
    database.session.commit()
    flash("Proprietário excluido com sucesso!")

    return redirect(url_for("feed"))

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.permissao < 2:
        return abort(403)
    
    proprietarios = Proprietario.query.all()
    
    # Total de ativos por categoria
    ativos = {}

    ativos = database.session.query(Ativo.tipo, database.func.sum(Ativo.quantidade_estoque)).group_by(Ativo.tipo).all()
    tipos_ativos = [ativo[0] for ativo in ativos]
    quantidades_ativos = [ativo[1] for ativo in ativos]

    # Total de ativos por departamento (total de saídas por departamento)
    total_ativos_departamento = defaultdict(int)

    for proprietario in proprietarios:
        for transacao in proprietario.transacoes:
            if transacao.tipo == 'Saída':
                total_ativos_departamento[proprietario.departamento] += int(transacao.quantidade)

    # Quantidade de ativos
    estoque = {}
    ativos = Ativo.query.all()
    for ativo in ativos:
        estoque[ativo.nome] = ativo.quantidade_estoque

    # Quantidade de solicitações abertas
    total_solicitacoes = defaultdict(int)
    solicitacoes = Solicitacao.query.all()

    for solicitacao in solicitacoes:
        total_solicitacoes[solicitacao.status] += 1
    
    return render_template("dashboard.html", labels=list(tipos_ativos), values=list(quantidades_ativos), 
                            total_labels=list(total_ativos_departamento.keys()), total_values=list(total_ativos_departamento.values()),
                            estoque_labels=list(estoque.keys()), estoque_values=list(estoque.values()),
                            solicitacoes_labels=list(total_solicitacoes.keys()), solicitacoes_values=list(total_solicitacoes.values()))

@app.route("/adicionar_estoque", methods=['GET', 'POST'])
@login_required
def adicionar_estoque():
    if current_user.permissao < 2:
        return abort(403)
    
    form = FormTransacaoEstoque()

    proprietarios = Proprietario.query.all()

    form.proprietario.choices = [(int(prop.id), prop.nome) for prop in proprietarios]

    ativos = Ativo.query.all()
    form.ativo.choices = [(int(atv.id), atv.nome) for atv in ativos]

    if form.validate_on_submit():
        ativo = Ativo.query.filter_by(id=form.ativo.data).first()
        
        transacao = TransacaoEstoque(tipo=form.tipo.data,
                                        descricao=form.descricao.data,
                                        quantidade=form.quantidade.data,
                                        id_ativo=form.ativo.data,
                                        id_proprietario=form.proprietario.data)

        if form.tipo.data == 'Entrada':
            ativo.quantidade_estoque += int(form.quantidade.data)
            
        elif form.tipo.data == 'Saída':
            ativo.quantidade_estoque -= int(form.quantidade.data)
        
        database.session.add(transacao)
        database.session.commit()
        return redirect(url_for('transacoes'))

    return render_template("adicionar_estoque.html", form=form)

@app.route("/estoque")
@login_required
def estoque():
    if current_user.permissao < 2:
        return abort(403)
    
    ativos = Ativo.query.all()
    return render_template("estoque.html", ativos=ativos)

@app.route("/solicitacoes")
@login_required
def solicitacoes():
    if current_user.permissao < 2:
        return abort(403)
    
    solicitacoes = Solicitacao.query.order_by(Solicitacao.data.desc()).all()
    return render_template("solicitacoes.html", solicitacoes=solicitacoes)

@app.route("/transacoes")
@login_required
def transacoes():
    if current_user.permissao < 2:
        return abort(403)
    
    transacoes = TransacaoEstoque.query.order_by(TransacaoEstoque.data.desc()).all()
    return render_template("transacoes.html", transacoes=transacoes)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    flash("Saiu com sucesso!")
    return redirect(url_for('index'))