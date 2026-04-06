# SkyBooker - Sistema de Reservas de Voos

Sistema web para gerenciamento de reservas de voos, desenvolvido com Django e PostgreSQL.

## Funcionalidades

- **Avioes**: Cadastro, listagem, edicao e exclusao de avioes com capacidade maxima de passageiros
- **Voos**: Gerenciamento de voos com origem, destino, data, horario e aviao associado
- **Clientes**: Cadastro de clientes com nome, email, CPF e telefone
- **Reservas**: Associacao de clientes a voos com numero de assento unico
- **Autenticacao**: Login/logout obrigatorio para acesso ao sistema
- **Interface grafica**: Interface web responsiva com Bootstrap 5

## Tecnologias

- Python 3.12+
- Django 6.0
- PostgreSQL
- Bootstrap 5
- HTML/CSS

## Pre-requisitos

- Python 3.12 ou superior
- PostgreSQL instalado e rodando
- Git

## Instalacao

1. Clone o repositorio:
```bash
git clone https://github.com/CgoulartS/desafio-dev.git
cd desafio-dev
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. Instale as dependencias:
```bash
pip install -r requirements.txt
```

4. Configure as variaveis de ambiente:
```bash
cp .env.example .env
```
Edite o arquivo `.env` com suas credenciais do PostgreSQL:
```
SECRET_KEY=sua-secret-key-aqui
DB_NAME=skybooker
DB_USER=seu-usuario
DB_PASSWORD=sua-senha
DB_HOST=localhost
DB_PORT=5432
```

5. Crie o banco de dados PostgreSQL:
```bash
psql -U seu-usuario -d postgres -c "CREATE DATABASE skybooker"
```

6. Execute as migracoes:
```bash
python manage.py migrate
```

7. Crie um superusuario:
```bash
python manage.py createsuperuser
```

8. Inicie o servidor:
```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## Testes

Execute os testes com:
```bash
python manage.py test voos -v2
```

## Admin

Acesse o painel administrativo em http://localhost:8000/admin/ com as credenciais do superusuario.

## Estrutura do Projeto

```
desafio-dev/
├── manage.py               # CLI do Django
├── requirements.txt        # Dependencias Python
├── .env.example            # Template de variaveis de ambiente
├── config/                 # Configuracao do projeto Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── voos/                   # App principal
│   ├── models.py           # Models: Aviao, Voo, Cliente, Reserva
│   ├── views.py            # Views CRUD (Class-Based Views)
│   ├── forms.py            # ModelForms com validacoes
│   ├── urls.py             # Rotas da app
│   ├── admin.py            # Configuracao do admin
│   └── tests.py            # Testes (22 testes)
├── templates/              # Templates HTML
│   ├── base.html           # Layout base com Bootstrap 5
│   ├── registration/       # Templates de autenticacao
│   └── voos/               # Templates CRUD
└── static/
    └── css/style.css       # Estilos customizados
```

## Regras de Negocio

- Cada aviao tem uma capacidade maxima de passageiros (> 0)
- Cada assento em um voo e unico (nao pode haver dois passageiros no mesmo assento)
- Um cliente so pode ter uma reserva por voo
- O numero total de reservas nao pode exceder a capacidade do aviao
- CPF e email de clientes sao unicos no sistema
