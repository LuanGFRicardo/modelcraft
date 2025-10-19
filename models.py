from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    def definir_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha, senha)


# ===== Novo: Tabela de Peças =====
class Peca(db.Model):
    __tablename__ = "pecas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    material = db.Column(db.String(100))
    arquivo_json = db.Column(db.String(200))

    # Medidas / peso e dimensões
    peso_kg = db.Column(db.Float)
    comprimento_mm = db.Column(db.Float)
    largura_mm = db.Column(db.Float)
    altura_mm = db.Column(db.Float)

    # Comercial
    preco = db.Column(db.Float)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    # Auditoria
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    @staticmethod
    def gerar_codigo():
        """Gera código único automático."""
        return f"PC-{uuid.uuid4().hex[:6].upper()}"

    def __repr__(self):
        return f"<Peca {self.codigo} - {self.nome}>"
