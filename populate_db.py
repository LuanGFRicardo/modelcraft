from app import criar_app
from extensions import db
from models import Produtos, Sensores, DadosColetados, Usuario  # Substitua Sensor por Sensores
from datetime import datetime
import random

# Criar a aplicação
app = criar_app()

# Adicionar dados ao banco de dados
with app.app_context():
    # Criar um produto
    produto = Produtos(nome='Produto Teste', descricao='Descrição do Produto Teste', empresa='Empresa Teste')
    db.session.add(produto)
    db.session.commit()

    # Criar um sensor associado ao produto
    sensor = Sensores(nome='Sensor de Teste', tipo='Tipo Teste', produto_id=produto.id)  # Substitua Sensor por Sensores
    db.session.add(sensor)
    db.session.commit()

    # Adicionar 20 dados coletados
    for i in range(20):
        dados = DadosColetados(
            sensor_id=sensor.id,
            data_hora=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            temperatura=random.uniform(20.0, 30.0),  # Temperatura aleatória entre 20 e 30
            umidade=random.uniform(30.0, 70.0),      # Umidade aleatória entre 30 e 70
            distancia_ultrassom=random.uniform(5.0, 100.0),  # Distância aleatória
            luminosidade_leds=random.uniform(100.0, 1000.0),  # Luminosidade aleatória
            status_bomba_agua='Ligada' if random.choice([True, False]) else 'Desligada',
            status_ventoinha='Ligada' if random.choice([True, False]) else 'Desligada'
        )
        db.session.add(dados)

    # Comitar as alterações
    db.session.commit()
    print("Dados populados com sucesso!")
