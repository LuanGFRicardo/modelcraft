from flask import Flask
from routes.auth import bp as auth_bp
from routes.main import bp as main_bp

def criar_app():
    """Função para criar a instância da aplicação Flask."""
    app = Flask(__name__)

    # Configurações do Flask
    app.config['SECRET_KEY'] = 'sua_chave_secreta'

    # Registrar as blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    return app
