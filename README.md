# Datathon - Seleção de Candidatos (RH)

O objetivo deste projeto é a criação de um modelo de machine learning que retorna a seleção dos melhores candidatos para uma determinada vaga. O modelo é implementado através de uma API desenvolvida com FastAPI que recebe o ID de uma vaga e retorna os 10 melhores candidatos.

O projeto inclui:

- Pré-processamento dos dados
- Treinamento do modelo
- Deploy do modelo através de uma API
- Testes unitários

Desenvolvido por: Bianca Gobe, Emerson Quirino e Mayara Reghin

Projeto desenvolvido para a pós-graduação em Machine Learning Engineering da FIAP

## 📁 Estrutura do projeto

Datathon

|   alembic.ini

|   app.db

|   database.db

|   docker-compose.yml

|   Dockerfile

|   poetry.lock

|   pyproject.toml

|   README.md

|   requirements.txt

|           

+---datathon

|   |   app.py

|   |   schemas.py

|   |   __init__.py

|   |   

|   +---core

|   |   |   settings.py

|   |   |   __init__.py

|   |   |              

|   +---db

|   |   |   database.py

|   |   |   models.py

|   |   |   __init__.py

|   |   |              

|   +---dependencies

|   |   |   security.py

|   |   |   __init__.py

|   |   |             

|   +---ml_models

|   |   |   applicants.json

|   |   |   applicants_preprocessed.parquet

|   |   |   Datathon_Fase5_Modelo.ipynb

|   |   |   modelo_supervisionado_rf.joblib

|   |   |   pre-processamento-embeddings

|   |   |   predict_service.py

|   |   |   prospects.json

|   |   |   vagas.json

|   |   |   vagas_preprocessed.parquet

|   |   |   __init__.py

|   |           

|   +---routers

|   |   |   auth.py

|   |   |   predict.py

|   |   |   users.py

|   |   |   __init__.py

|   |   |   

|       

+---migrations

|   |   env.py

|   |   README

|           

+---tests

|   |   conftest.py

|   |   test_app.py

|   |   test_auth.py

|   |   test_db.py

|   |   test_predict.py

|   |   test_users.py

|   |   __init__.py

|

**Arquivos principais na raiz**

- alembic.ini → Configuração do Alembic para controle de migrações de banco de dados.
- app.db / database.db → Bancos de dados SQLite usados pelo projeto.
- docker-compose.yml → Arquivo para orquestração de containers Docker.
- Dockerfile → Arquivo para criar a imagem Docker do projeto.
- pyproject.toml / poetry.lock → Arquivos de configuração do Poetry (gerenciamento de dependências).
- requirements.txt → Dependências do projeto (para quem não usar Poetry).
- README.md → Documentação do projeto.

**Pasta datathon**

Contém o núcleo da aplicação:
- app.py → Arquivo principal que inicializa a API FastAPI.
- schemas.py → Definição de schemas para requisições e respostas da API.

Subpastas

- core
  
settings.py → Configurações centrais do projeto, incluindo variáveis de ambiente.

- db

database.py → Configuração da conexão com o banco de dados SQLite.
models.py → Definição das tabelas e modelos do banco de dados.

- dependencies

security.py → Funções relacionadas a autenticação e segurança da API.

- ml_models

Contém dados de entrada (.json, .parquet), notebooks e scripts de machine learning.
predict_service.py → Serviço responsável por fazer previsões usando os modelos treinados.

- routers

Contém os endpoints da API, separados por funcionalidade:
auth.py → Autenticação e gerenciamento de tokens.
predict.py → Endpoints para fazer predições com os modelos.
users.py → Endpoints de gerenciamento de usuários.

**Pasta migrations**

Contém arquivos gerados pelo Alembic para controle de versão do banco de dados.

**Pasta tests**

Contém testes unitários e de integração para a aplicação, garantindo que endpoints, modelos e banco de dados funcionem corretamente.
Arquivos como test_app.py, test_auth.py, test_db.py, test_predict.py e test_users.py cobrem diferentes partes do sistema

## 🛠️ Tecnologias utilizadas
- 📦 Python
- 🧠 BERT e Scikit-learn – Treinamento do modelo LSTM
- 📊 Pandas e Numpy – Manipulação e pré-processamento de dados
- 🚀 FastAPI – Criação da API REST
- 🐳 Docker – Containerização da aplicação
- ☁️ AWS EC2 e AWS Cloudwatch - Deploy e monitoramento da aplicação em nuvem

## 📊 Sobre o modelo

Este modelo tem como objetivo oferecer ao time da Decision o top 10 candidatos mais compatíveis por vaga e demostrar o score de compatibilidade. O modelo criar um classificador que aprenda a distinguir entre candidatos relevantes (positivos) e irrelevantes (negativos) para cada vaga, com base em:

- A descrição da vaga
- O conteúdo do currículo do candidato
- Informações estruturadas (área, nível, escolaridade e etc.)

O código do treinamento do modelo está disponível também no Google Colab: [Colab](https://colab.research.google.com/drive/1Wu2GYyibUWa7IpVuFgtOKk6uuAHHDJq0?usp=sharing#scrollTo=PAGF9ZGaecla)

## 🚀 Funcionalidades da API

**Previsão dos melhores candidatos para uma vaga:** Retorno de um ranking com os 10 melhores candidatos a partir do ID de uma vaga

**Retorno das informações das vagas e candidatos:** Retorno das informações das vagas e candidatos a partir do ID.

**Autenticação:** As rotas da API são protegidas por autenticação JWT (JSON Web Token), garantindo maior segurança e controle de acesso. Os usuários podem criar suas contas, alterar seus dados, consultar e deletar sua conta. O token é válido por 30 minutos a partir do momento do login e pode ser reiniciado.

**Testes Unitários**: Todas as rotas são testadas através de testes unitários com PyTest.

**Documentação:** Documentação automática com Swagger

## 📍 Documentação do projeto

Confira todos os detalhes e explicações do projeto na documentação: [Documentação em PDF](link)

Veja também o vídeo apresentando o projeto: [Vídeo](link)

## 🧪 Como Executar o Projeto

0. Pré-requisitos

- Instalação do Python 3.10+
- Instalação do Docker e Docker Compose

1. Clone o Repositório
```bash
git clone [https://github.com/mayarareghin/datathon-selecao-candidatos-rh.git]
```

2. Baixe as bases de dados e o modelo salvo em joblib através do link abaixo (arquivos grandes) e salve em "datathon/ml_models/"

🔗 [Google Drive](https://drive.google.com/drive/folders/1oVsvJFR1POPneoScvX1JwxYco7lfPHDE)

4. Crie o arquivo .env na raiz do projeto com o conteúdo abaixo:
```bash
DATABASE_URL="postgresql+asyncpg://datathon:datathonpas@db:5432/app_db"
ALGORITHM="HS256"
SECRET_KEY="senha123"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Construa o container Docker
```bash
docker build -t datathon-minha_api .
```

5 Suba o container
```bash
docker run -d --name datathon-container -p 8000:8000 --env-file .env datathon-minha_api
```

6 Rode as migraçõs Alembic dentro do container
```bash
docker exec -it datathon-container bash
alembic upgrade head
exit
```

7 Acesse a aplicação em : http://localhost:8000


### 🤝 Contribuindo
Fork este repositório.
Crie sua branch (git checkout -b feature/nova-funcionalidade).
Faça commit das suas alterações (git commit -m 'Adiciona nova funcionalidade').
Faça push para sua branch (git push origin feature/nova-funcionalidade).
Abra um Pull Request. instalar, configurar e usar o projeto. Ele também cobre contribuições, contato, licença e agradecimentos, tornando-o completo e fácil de entender para novos desenvolvedores.
