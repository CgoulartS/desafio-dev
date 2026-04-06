# SkyBooker - Sistema de Reservas de Voos

Sistema web para gerenciamento de reservas de voos, desenvolvido com **Django** e **PostgreSQL**.

## Funcionalidades

### Requisitos Obrigatorios
- **Cadastro de Avioes**: CRUD completo com modelo, fabricante e capacidade maxima de passageiros
- **Gerenciamento de Voos**: CRUD com aviao associado, origem, destino, data e horario
- **Cadastro de Clientes**: CRUD com nome, email (unico), CPF (unico) e telefone
- **Reservas de Assentos**: Associacao de clientes a voos com assento unico por reserva

### Regras de Negocio
- Cada assento em um voo e unico (constraint no banco)
- Um cliente so pode ter uma reserva por voo (constraint no banco)
- O numero total de reservas nao pode exceder a capacidade do aviao
- Numero do assento deve estar entre 1 e a capacidade maxima do aviao
- CPF deve conter exatamente 11 digitos numericos

### Bonus
- **Interface grafica** responsiva com Bootstrap 5
- **Autenticacao** com login/logout obrigatorio

### Diferenciais
- **Dashboard** com metricas: totais, taxa de ocupacao media, proximos voos
- **Busca e filtros**: voos por origem/destino/data, clientes por nome/email/CPF
- **Paginacao** em todas as listagens (10 itens por pagina)
- **Selecao visual de assentos**: mapa interativo (verde = disponivel, vermelho = ocupado)
- **UUID como PK**: todas as entidades usam UUID ao inves de IDs incrementais (previne ataques IDOR)
- **Controle de acesso (RBAC)**: usuarios staff vs usuarios comuns com permissoes distintas
- **Privacidade**: usuarios comuns veem apenas suas proprias reservas
- **Service layer**: logica de negocio separada das views
- **Arquitetura modular**: models, views, forms e testes separados por entidade

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
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
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

O projeto possui **30 testes automatizados** organizados por entidade, cobrindo models, forms, views, RBAC, privacidade, busca, paginacao e endpoints JSON.

```bash
python manage.py test voos -v2
```

## Controle de Acesso

| Acao | Staff (admin) | Usuario comum |
|------|:---:|:---:|
| Ver dashboard | Sim | Sim |
| Listar avioes/voos/clientes | Sim | Sim |
| Criar/editar/excluir avioes | Sim | Nao (403) |
| Criar/editar/excluir voos | Sim | Nao (403) |
| Criar/editar/excluir clientes | Sim | Nao (403) |
| Criar reserva | Sim | Sim |
| Ver reservas | Todas | Apenas as suas |
| Cancelar reserva | Todas | Apenas as suas |

## Arquitetura

```
voos/
├── models/                  # 1 arquivo por entidade
│   ├── aviao.py             #   UUID PK, modelo, fabricante, max_passageiros
│   ├── voo.py               #   UUID PK, FK aviao, properties (assentos_disponiveis, esta_lotado)
│   ├── cliente.py            #   UUID PK, FK usuario (User), email/cpf unique
│   └── reserva.py            #   UUID PK, UniqueConstraints (voo+assento, voo+cliente)
├── views/                   # 1 arquivo por entidade
│   ├── mixins.py            #   StaffRequiredMixin (RBAC)
│   ├── home.py              #   Dashboard (delega para DashboardService)
│   ├── aviao.py             #   CRUD (StaffRequired para CUD)
│   ├── voo.py               #   CRUD + busca + endpoint JSON assentos
│   ├── cliente.py            #   CRUD + busca (StaffRequired para CUD)
│   └── reserva.py            #   CRUD com filtro de privacidade
├── forms/                   # 1 arquivo por entidade
│   ├── aviao_form.py        #   Validacao max_passageiros > 0
│   ├── voo_form.py          #   Widgets date/time
│   ├── cliente_form.py       #   Validacao CPF 11 digitos
│   └── reserva_form.py      #   Delega validacoes para ReservaService
├── services/                # Camada de servico (logica de negocio)
│   ├── reserva_service.py   #   Validacoes: assento, capacidade, cliente unico
│   └── dashboard_service.py #   Calculo de metricas (totais, ocupacao, proximos voos)
├── tests/                   # 1 arquivo por entidade
│   ├── base.py              #   BaseTestCase (staff) + RegularUserTestCase
│   ├── test_aviao.py        #   Model, View, RBAC
│   ├── test_voo.py          #   Model, View, Assentos endpoint
│   ├── test_cliente.py       #   Model, View, unique constraints
│   ├── test_reserva.py      #   Model, Form, View, Privacidade
│   ├── test_dashboard.py    #   Metricas vazias e com dados
│   └── test_pagination.py   #   Paginacao
├── admin.py                 # search_fields, list_filter, date_hierarchy
└── urls.py                  # UUID routes (<uuid:pk>)
```

## Modelo de Dados

```
Aviao (1) ──── (N) Voo (1) ──── (N) Reserva (N) ──── (1) Cliente ──── (1) User
  id (UUID)          id (UUID)         id (UUID)           id (UUID)
  modelo             aviao (FK)        voo (FK)            usuario (FK → User)
  fabricante         origem            cliente (FK)        nome
  max_passageiros    destino           numero_assento      email (unique)
                     data              criado_em           cpf (unique)
                     horario                               telefone

Constraints:
  UNIQUE(voo, numero_assento) — assento unico por voo
  UNIQUE(voo, cliente) — um cliente por voo
```
