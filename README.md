# SkyBooker - Sistema de Reservas de Voos

Sistema web completo para gerenciamento de reservas de voos, desenvolvido com **Django** e **PostgreSQL**.

## Funcionalidades

### Requisitos Obrigatorios
- **Cadastro de Avioes**: CRUD completo com modelo, fabricante e capacidade maxima de passageiros
- **Gerenciamento de Voos**: CRUD com aviao associado, origem, destino, data e horario
- **Cadastro de Clientes**: CRUD com nome, email (unico), CPF (unico) e telefone
- **Reservas de Assentos**: Associacao de clientes a voos com assento unico por reserva

### Regras de Negocio
- Cada assento em um voo e unico (nao pode haver dois passageiros no mesmo assento)
- Um cliente so pode ter uma reserva por voo
- O numero total de reservas nao pode exceder a capacidade do aviao
- Numero do assento deve estar entre 1 e a capacidade maxima do aviao
- CPF deve conter exatamente 11 digitos numericos

### Bonus
- **Interface grafica** responsiva com Bootstrap 5
- **Autenticacao** (login/logout obrigatorio para acesso ao sistema)

### Diferenciais
- **Dashboard** com metricas: totais de avioes, voos, clientes, reservas, taxa de ocupacao media e proximos voos
- **Busca e filtros**: voos por origem/destino/data, clientes por nome/email/CPF
- **Paginacao** em todas as listagens (10 itens por pagina)
- **Selecao visual de assentos**: mapa interativo mostrando assentos disponiveis (verde) e ocupados (vermelho) ao criar reserva

## Tecnologias

| Tecnologia | Versao | Uso |
|-----------|--------|-----|
| Python | 3.12+ | Linguagem backend |
| Django | 6.0 | Framework web |
| PostgreSQL | 14+ | Banco de dados |
| Bootstrap | 5.3 | Interface responsiva (via CDN) |
| HTML/CSS/JS | - | Frontend (templates Django + JS vanilla) |

## Pre-requisitos

- **Python 3.12** ou superior
- **PostgreSQL** instalado e rodando
- **Git**

## Instalacao e Execucao

### 1. Clone o repositorio

```bash
git clone https://github.com/CgoulartS/desafio-dev.git
cd desafio-dev
```

### 2. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate    # Linux/macOS
# venv\Scripts\activate     # Windows
```

### 3. Instale as dependencias

```bash
pip install -r requirements.txt
```

**Dependencias (requirements.txt):**
- `Django>=5.0,<7.0` — Framework web
- `psycopg2-binary>=2.9` — Driver PostgreSQL para Python
- `python-dotenv>=1.0` — Carregamento de variaveis de ambiente

### 4. Configure as variaveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
SECRET_KEY=django-insecure-troque-por-uma-chave-segura
DB_NAME=skybooker
DB_USER=seu-usuario-postgres
DB_PASSWORD=sua-senha
DB_HOST=localhost
DB_PORT=5432
```

### 5. Crie o banco de dados

```bash
psql -U seu-usuario -d postgres -c "CREATE DATABASE skybooker"
```

### 6. Execute as migracoes

```bash
python manage.py migrate
```

### 7. Crie um superusuario

```bash
python manage.py createsuperuser
```

### 8. Inicie o servidor

```bash
python manage.py runserver
```

Acesse: **http://localhost:8000**

## Testes

O projeto possui **34 testes automatizados** cobrindo models, forms, views, autenticacao, busca, paginacao e endpoint de assentos.

```bash
python manage.py test voos -v2
```

## Uso do Sistema

1. Acesse http://localhost:8000 e faca login com o superusuario criado
2. O **Dashboard** mostra as metricas gerais do sistema
3. Use o menu de navegacao para acessar **Avioes**, **Voos**, **Clientes** e **Reservas**
4. Ao criar uma reserva, selecione o voo para ver o **mapa de assentos** interativo
5. Use os campos de **busca** nas listagens de voos e clientes
6. O painel administrativo esta disponivel em http://localhost:8000/admin/

## Estrutura do Projeto

```
desafio-dev/
├── manage.py                # CLI do Django
├── requirements.txt         # Dependencias Python
├── .env.example             # Template de variaveis de ambiente
├── README.md                # Este arquivo
├── config/                  # Configuracao do projeto Django
│   ├── settings.py          # Settings (PostgreSQL, Bootstrap, auth)
│   ├── urls.py              # Rotas raiz
│   ├── wsgi.py              # WSGI entry point
│   └── asgi.py              # ASGI entry point
├── voos/                    # App principal
│   ├── models.py            # 4 Models: Aviao, Voo, Cliente, Reserva
│   ├── views.py             # 18 Views (CBVs) + endpoint JSON
│   ├── forms.py             # 4 ModelForms com validacoes de negocio
│   ├── urls.py              # 21 rotas
│   ├── admin.py             # Admin com list_display
│   └── tests.py             # 34 testes automatizados
├── templates/               # Templates HTML
│   ├── base.html            # Layout base (Bootstrap 5, navbar, mensagens)
│   ├── registration/        # Login e logout
│   └── voos/                # Templates CRUD + dashboard + paginacao
└── static/
    └── css/style.css        # Estilos customizados
```

## Modelo de Dados

```
Aviao (1) ──── (N) Voo (1) ──── (N) Reserva (N) ──── (1) Cliente
  - modelo            - aviao (FK)       - voo (FK)           - nome
  - fabricante        - origem           - cliente (FK)       - email (unique)
  - max_passageiros   - destino          - numero_assento     - cpf (unique)
                      - data             - criado_em          - telefone
                      - horario

Constraints:
  UNIQUE(voo, numero_assento) — assento unico por voo
  UNIQUE(voo, cliente) — um cliente por voo
```
