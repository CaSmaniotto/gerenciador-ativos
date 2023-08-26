from flask import render_template, url_for, redirect, flash, session, request
from aplicacao import app, database, bcrypt
from aplicacao.models import Usuario, Ativo, Proprietario
from flask_login import login_required, login_user, logout_user, current_user
from aplicacao.forms import FormLogin, FormCriarConta, FormAtivos, FormProprietario
from sqlalchemy import asc
from sqlalchemy.sql import func


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
        return redirect('/')

    return render_template("registrar.html", form=form)

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/ativo", methods=["GET", "POST"])
@login_required
def ativo():
    form = FormAtivos()

    proprietarios = Proprietario.query.all()
    form.proprietario.choices = [(int(prop.id), prop.nome) for prop in proprietarios]

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
                        status=form.status.data,
                        id_proprietario=form.proprietario.data)
            database.session.add(ativo)
            database.session.commit()
            flash("ativo criado com sucesso!")
            return redirect('/feed')

    return render_template("cadastrar_ativo.html", form=form)

@app.route("/proprietario", methods=["GET", "POST"])
@login_required
def proprietario():
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
                                        departamento=form.departamento.data)
            database.session.add(proprietario)
            database.session.commit()
            flash("Proprietário cadastrado!")
            return redirect('/feed')
    return render_template("cadastrar_proprietario.html", form=form)

@app.route("/feed")
@login_required
def feed():
    proprietarios = Proprietario.query.all()
    ativos = Ativo.query.all()
    return render_template("feed.html", ativos=ativos, proprietarios=proprietarios)

@app.route("/get_item/<string:item_type>/<string:action>/<int:item_id>")
@login_required
def get_item(item_type, action, item_id):
    session['item_id'] = item_id
    
    if item_type == 'ativo':
        if action == 'edit':
            return redirect(url_for("edit_ativo"))
        elif action == 'delete':
            return redirect(url_for("delete_ativo"))
    elif item_type == 'proprietario':
        if action == 'edit':
            return redirect(url_for("edit_proprietario"))
        elif action == 'delete':
            return redirect(url_for("delete_proprietario"))
    else:
        return redirect("feed")

@app.route("/feed/edit_ativo", methods=["GET", "POST"])
@login_required
def edit_ativo():
    ativo_id = session.get('item_id')
    ativo = Ativo.query.get(int(ativo_id))

    form_edit = FormAtivos(obj=ativo)

    # Definindo os campos do form
    form_edit.proprietario.choices = [(prop.id, prop.nome) for prop in Proprietario.query.all()]

    if form_edit.validate_on_submit():
        # form_edit.populate_obj(ativo)
        ativo.nome = form_edit.nome.data
        ativo.tipo =form_edit.tipo.data
        ativo.descricao = form_edit.descricao.data
        ativo.data_aquisicao = form_edit.data_aquisicao.data
        ativo.data_garantia = form_edit.data_garantia.data
        ativo.status = form_edit.status.data
        ativo.id_proprietario = form_edit.proprietario.data

        database.session.commit()
        flash("Editado com sucesso!")
        return redirect('/feed')
    elif request.method == 'GET':
        form_edit.proprietario.data = str(ativo.proprietario.id)
        return render_template("edit_ativo.html", form=form_edit) 

@app.route("/delete_ativo")
@login_required
def delete_ativo():
    ativo = Ativo.query.get(session.get('item_id'))
    database.session.delete(ativo)
    database.session.commit()
    flash("Ativo excluido com sucesso!")
    return redirect(url_for("feed"))

@app.route("/feed/edit_proprietario", methods=["GET", "POST"])
@login_required
def edit_proprietario():
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
            return redirect('/feed')
        else:
            flash("CPF já utilizado!")

    return render_template("edit_proprietario.html", form=form_edit)

@app.route("/delete_proprietario")
@login_required
def delete_proprietario():
    proprietario = Proprietario.query.get(session.get('item_id'))
    database.session.delete(proprietario)
    database.session.commit()
    flash("Proprietário excluido com sucesso!")
    return redirect(url_for("feed"))

@app.route("/dashboard")
@login_required
def dashboard():
    dados = {}
    status_choices = FormAtivos().status.choices
    for status_value, _ in status_choices:
        status_count = Ativo.query.filter_by(status=status_value).count()
        dados[status_value] = status_count
        # print(f"Status: {status_value}, Contagem: {status_count}")
    
    return render_template("dashboard.html", labels=list(dados.keys()), values=list(dados.values()))


@app.route("/logout")
@login_required
def logout():
    # session.pop('usuario', None)
    session.clear()
    logout_user()
    flash("Saiu com sucesso!")
    return redirect(url_for('index'))