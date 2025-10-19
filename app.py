# Bibliotecas
from flask import Flask
from config import Config
from extensions import db, login_manager
from routes.auth import bp as auth_bp
from routes.main import bp as main_bp
from models import Usuario

# Criar a aplicação
def criar_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Define a página de login padrão
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "erro"

    # Definir o carregador de usuário
    @login_manager.user_loader
    def carregar_usuario(usuario_id):
        return Usuario.query.get(int(usuario_id))

    # Registrar Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    return app

# Iniciar a aplicação
if __name__ == "__main__":
    app = criar_app()
    with app.app_context():
        db.create_all()  # Criar o banco de dados
    app.run(host='0.0.0.0', port=7000, debug=True)
