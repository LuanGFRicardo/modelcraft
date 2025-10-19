# Bibliotecas
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from extensions import db
from models import Usuario, Peca
import uuid, os

# Definir rota de autenticação
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Rota de login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  # Redireciona se já estiver autenticado
    
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(nome_usuario=nome_usuario).first()
        
        if usuario and usuario.checar_senha(senha):
            login_user(usuario)
            return redirect(url_for('main.home'))  # Redireciona após login bem-sucedido
        
        flash('Login inválido. Verifique o nome de usuário e/ou a senha.', 'erro')
    return render_template('login.html')

# Rota de registro
@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        email = request.form['email']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)
        usuario = Usuario(nome_usuario=nome_usuario, email=email, senha=senha_hash)
        
        try:
            db.session.add(usuario)
            db.session.commit()
            flash('Sua conta foi criada! Você agora pode fazer login.', 'sucesso')  # Mensagem de sucesso
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
            flash('Erro ao criar a conta. Nome de usuário ou e-mail já existe.', 'erro')  # Mensagem de erro
    
    return render_template('register.html')

# Rota de logout
@bp.route('/sair')
@login_required
def sair():
    logout_user()
    return redirect(url_for('auth.confirmacao_logout'))

# Rota de confirmação de logout
@bp.route('/confirmacao_logout')
def confirmacao_logout():
    return render_template('confirmacao_logout.html')

# 
@bp.route('/listagem')
@login_required
def listagem():
    pecas = Peca.query.order_by(Peca.created_at.desc()).all()
    return render_template('listagem.html', pecas=pecas, current_user=current_user)

# 
@bp.route('/nova_peca')
@login_required
def nova_peca():
    return render_template('criar_peca.html')

# 
@bp.route('/salvar_peca_automatica', methods=['POST'])
@login_required
def salvar_peca_automatica():
    nome = request.form.get('nome')
    material = request.form.get('material')
    preco = request.form.get('preco')
    comprimento = request.form.get('comprimento_mm')
    largura = request.form.get('largura_mm')
    altura = request.form.get('altura_mm')
    peso = request.form.get('peso_kg')
    arquivo = request.files.get('meshFile')

    if not nome or not arquivo:
        flash('Nome e arquivo são obrigatórios.', 'erro')
        return redirect(url_for('auth.nova_peca'))

    # Salva o arquivo em /uploads
    upload_dir = 'uploads'
    os.makedirs(upload_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{arquivo.filename}"
    filepath = os.path.join(upload_dir, filename)
    arquivo.save(filepath)

    peca = Peca(
        nome=nome.strip(),
        codigo=Peca.gerar_codigo(),
        material=material.strip() if material else None,
        preco=float(preco) if preco else None,
        comprimento_mm=float(comprimento) if comprimento else None,
        largura_mm=float(largura) if largura else None,
        altura_mm=float(altura) if altura else None,
        peso_kg=float(peso) if peso else None,
        arquivo_json=filename,
        ativo=True
    )
    db.session.add(peca)
    db.session.commit()
    flash(f'Peça "{nome}" criada automaticamente com sucesso!', 'sucesso')
    return redirect(url_for('auth.listagem'))

# Editar peça (formulário)
@bp.route('/peca/<int:id>/editar', methods=['GET'])
@login_required
def editar_peca(id):
    peca = Peca.query.get_or_404(id)
    return render_template('editar_peca.html', peca=peca)

# Atualizar peça (submit do form de edição)
@bp.route('/peca/<int:id>/atualizar', methods=['POST'])
@login_required
def atualizar_peca(id):
    peca = Peca.query.get_or_404(id)

    # Campos básicos
    peca.nome = (request.form.get('nome') or '').strip() or peca.nome
    peca.material = (request.form.get('material') or None) or peca.material

    # Conversões numéricas simples (mantendo a mesma lógica de tipos)
    def f(v, casas=None):
        if v is None or v == '': return None
        v = v.replace('.', '').replace(',', '.')  # aceita vírgula
        try:
            num = float(v)
            if casas is not None:
                return float(f"{num:.{casas}f}")
            return num
        except ValueError:
            return None

    peca.preco = f(request.form.get('preco'), 2)
    peca.comprimento_mm = f(request.form.get('comprimento_mm'), 3)
    peca.largura_mm = f(request.form.get('largura_mm'), 3)
    peca.altura_mm = f(request.form.get('altura_mm'), 3)
    peca.peso_kg = f(request.form.get('peso_kg'), 3)

    # Troca opcional do arquivo (mantendo funcionalidade)
    arquivo = request.files.get('meshFile')
    if arquivo and arquivo.filename:
        upload_dir = 'uploads'
        os.makedirs(upload_dir, exist_ok=True)
        filename = f"{uuid.uuid4().hex}_{arquivo.filename}"
        arquivo.save(os.path.join(upload_dir, filename))
        peca.arquivo_json = filename

    try:
        db.session.commit()
        flash('Peça atualizada com sucesso!', 'sucesso')
    except Exception:
        db.session.rollback()
        flash('Erro ao atualizar a peça.', 'erro')

    return redirect(url_for('auth.listagem'))

# Excluir peça
@bp.route('/peca/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_peca(id):
    peca = Peca.query.get_or_404(id)
    try:
        db.session.delete(peca)
        db.session.commit()
        flash('Peça excluída com sucesso!', 'sucesso')
    except Exception:
        db.session.rollback()
        flash('Erro ao excluir a peça.', 'erro')
    return redirect(url_for('auth.listagem'))

#
@bp.route('/calcular', methods=['GET'])
@login_required
def calcular():
    # Carrega peças para o seletor
    pecas = Peca.query.order_by(Peca.nome.asc()).all()
    return render_template('calcular.html', pecas=pecas, current_user=current_user)

