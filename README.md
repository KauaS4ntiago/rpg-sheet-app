# 🎲 Ficha Web App

Aplicação web para criação e gerenciamento de fichas de personagens de RPG.

O projeto foi desenvolvido como uma aplicação **full-stack**, com uma API REST em **Python/Flask** e uma interface web em **React**, permitindo cadastrar usuários, criar personagens e gerenciar seus atributos, habilidades e informações da ficha.


## ✨ Funcionalidades

* 🔐 Cadastro e autenticação de usuários
* 👤 Criação e gerenciamento de personagens
* 📋 Criação e edição de fichas de RPG
* ❤️ Gerenciamento de pontos de vida
* 🧠 Gerenciamento de sanidade
* 📊 Gerenciamento de atributos
* ⚔️ Gerenciamento de habilidades e capacidades
* 🖼️ Upload de imagem para personagens
* 🔄 Comunicação entre frontend e API REST
* 🗄️ Persistência dos dados em banco de dados

## 🛠️ Tecnologias utilizadas

### Backend

* **Python**
* **Flask**
* **Flask-SQLAlchemy**
* **Flask-JWT-Extended**
* **MySQL**
* **REST API**
* **CORS**

### Frontend

* **React**
* **Vite**
* **JavaScript**
* **HTML5**
* **CSS3**

### Ferramentas

* **Git**
* **GitHub**

## 📁 Estrutura do projeto

```text
Ficha-Web-App/
├── backend/
│   ├── ...
│   └── API Flask
│
├── frontend/
│   ├── ...
│   └── Aplicação React
│
└── .gitignore
```

O projeto é dividido em duas partes principais:

* **`backend/`** — responsável pela API, autenticação, regras de negócio e comunicação com o banco de dados.
* **`frontend/`** — responsável pela interface da aplicação e interação com a API.

## 🔐 Autenticação

A aplicação utiliza **JWT (JSON Web Token)** para autenticação e autorização dos usuários.

Após o login, o token é utilizado nas requisições que necessitam de autenticação, permitindo que cada usuário tenha acesso aos seus próprios personagens e dados.

## 🔌 API

O backend disponibiliza uma API REST para comunicação com o frontend.

Entre os principais recursos estão:

```text
/auth
/users
/characters
/attributes
/skills
/abilities
```

A API é responsável pelas operações de criação, consulta, atualização e exclusão dos dados da aplicação.

## 🚀 Como executar o projeto localmente

### Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

* [Python](https://www.python.org/)
* [Node.js](https://nodejs.org/)
* [MySQL](https://www.mysql.com/)
* Git

### 1. Clone o repositório

```bash
git clone https://github.com/KauaS4ntiago/Ficha-Web-App.git

cd Ficha-Web-App
```

### 2. Configuração do Backend

Entre na pasta do backend:

```bash
cd backend
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure as variáveis de ambiente necessárias para conexão com o banco de dados e autenticação.

Depois, execute a API:

```bash
python app.py
```

O backend será iniciado, por padrão, na porta:

```text
http://localhost:5000
```

### 3. Configuração do Frontend

Em outro terminal:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Execute o projeto:

```bash
npm run dev
```

O frontend será disponibilizado pelo Vite, normalmente em:

```text
http://localhost:5173
```

## 🗄️ Banco de dados

O projeto utiliza **MySQL** para armazenamento dos dados.

Entre as principais entidades estão:

* Usuários
* Personagens
* Atributos
* Habilidades
* Capacidades

O relacionamento entre essas entidades permite que cada usuário mantenha seus próprios personagens e suas respectivas informações.

## 🎯 Objetivo do projeto

Este projeto foi desenvolvido com o objetivo de colocar em prática conceitos de desenvolvimento **Back-end e Full-Stack**, incluindo:

* Desenvolvimento de APIs REST
* Autenticação com JWT
* Integração entre frontend e backend
* Modelagem e relacionamento de banco de dados
* Operações CRUD
* Desenvolvimento de interfaces com React
* Organização de aplicações web
* Integração entre diferentes tecnologias

Além de ser uma aplicação funcional, o projeto também serve como experiência prática no desenvolvimento de sistemas completos.

## 📌 Próximos passos

Algumas melhorias planejadas para o projeto:

* [ ] Melhorar a documentação da API
* [ ] Adicionar testes automatizados
* [ ] Melhorar o sistema de validação de dados
* [ ] Aprimorar o tratamento de erros
* [ ] Melhorar a responsividade da interface
* [ ] Adicionar novas funcionalidades para as fichas
* [ ] Melhorar o sistema de deploy

## 👨‍💻 Autor

**Kauã Santiago**

Estudante de Sistemas de Informação e desenvolvedor Back-end em formação, com foco em Python, Flask, SQL e desenvolvimento de APIs REST.

🔗 **GitHub:** [KauaS4ntiago](https://github.com/KauaS4ntiago)

---

⭐ Se este projeto foi útil ou interessante para você, considere deixar uma estrela no repositório!
