# Datathon - Seleção de Candidatos (RH)

Projeto final da pós-graduação em Engenharia de Machine Learning na FIAP, com a criação de um modelo de machine learning que retorna a seleção dos melhores candidatos para uma determinada vaga. O modelo é implementado através de uma API desenvolvida com FastAPI que recebe o ID de uma vaga e retorna os 10 melhores candidatos.

O projeto inclui:

- Tratamento de dados
- Treinamento do modelo
- Deploy do modelo através da AI
- Testes unitários

Desenvolvido por: Bianca Gobe, Emerson Quirino e Mayara Reghin

Projeto desenvolvido para a pós-graduação em Machine Learning Engineering da FIAP

## 📁 Estrutura do projeto

## 🛠️ Tecnologias utilizadas
- 📦 Python
- 🧠 BERT e Scikit-learn – Treinamento do modelo LSTM
- 📊 Pandas e Numpy – Manipulação e pré-processamento de dados
- 🚀 FastAPI – Criação da API REST
- 🐳 Docker – Containerização da aplicação
- ☁️ AWS EC2 e AWS Cloudwatch - Deploy e monitoramento da aplicação em nuvem

## Sobre o modelo

O código do treinamento do modelo está disponível também no Google Colab: [Colab](https://colab.research.google.com/drive/1Wu2GYyibUWa7IpVuFgtOKk6uuAHHDJq0?usp=sharing#scrollTo=PAGF9ZGaecla)

## 🚀 Funcionalidades da API

**Previsão dos melhores candidatos para uma vaga:** Retorno de um ranking com os 10 melhores candidatos a partir do ID de uma vaga

**Autenticação:** As rotas da API são protegidas por autenticação JWT (JSON Web Token), garantindo maior segurança e controle de acesso. Os usuários podem criar suas contas, alterar seus dados, consultar e deletar sua conta. O token é válido por 30 minutos a partir do momento do login e pode ser reiniciado.

**Testes Unitários**: Todas as rotas são testadas através de testes unitários com PyTest.

**Documentação:** Documentação automática com Swagger

## 📍 Documentação do projeto

Confira todos os detalhes e explicações do projeto na documentação: [Documentação em PDF](link)

Veja também o vídeo apresentando o projeto: [Vídeo](link)

## 🧪 Como Executar o Projeto

### 🤝 Contribuindo
Fork este repositório.
Crie sua branch (git checkout -b feature/nova-funcionalidade).
Faça commit das suas alterações (git commit -m 'Adiciona nova funcionalidade').
Faça push para sua branch (git push origin feature/nova-funcionalidade).
Abra um Pull Request. instalar, configurar e usar o projeto. Ele também cobre contribuições, contato, licença e agradecimentos, tornando-o completo e fácil de entender para novos desenvolvedores.