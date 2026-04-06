# SkyBooker - Sistema de Reservas de Voos

Sistema web para gerenciamento de reservas de voos, desenvolvido com **Django** e **PostgreSQL**.

## Funcionalidades

### Requisitos Obrigatórios
- **Cadastro de Aviões**: CRUD completo com modelo, fabricante e capacidade máxima de passageiros
- **Gerenciamento de Voos**: CRUD com avião associado, origem, destino, data e horário
- **Cadastro de Clientes**: CRUD com nome, email (único), CPF (único) e telefone
- **Reservas de Assentos**: Associação de clientes a voos com assento único por reserva

### Regras de Negócio
- Cada assento em um voo é único (constraint no banco)
- Um cliente só pode ter uma reserva por voo (constraint no banco)
- O número total de reservas não pode exceder a capacidade do avião
- Número do assento deve estar entre 1 e a capacidade máxima do avião
- CPF deve conter exatamente 11 dígitos numéricos

### Bônus
- **Interface gráfica** responsiva com Bootstrap 5
- **Autenticação** com login/logout obrigatório

### Diferenciais
- **Dashboard** com métricas: totais, taxa de ocupação média, próximos voos
- **Busca e filtros**: voos por origem/destino/data, clientes por nome/email/CPF
- **Paginação** em todas as listagens (10 itens por página)
- **Seleção visual de assentos**: mapa interativo (verde = disponível, vermelho = ocupado)
- **UUID como PK**: todas as entidades usam UUID ao invés de IDs incrementais (previne ataques IDOR)
- **Controle de acesso (RBAC)**: usuários staff vs usuários comuns com permissões distintas
- **Privacidade**: usuários comuns veem apenas suas próprias reservas
- **Service layer**: lógica de negócio separada das views
- **Arquitetura modular**: models, views, forms e testes separados por entidade
- **Design system customizado**: identidade visual própria com CSS tokens

## Tecnologias

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Python | 3.12+ | Linguagem backend |
| Django | 6.0 | Framework web |
| PostgreSQL | 14+ | Banco de dados |
| Bootstrap | 5.3 | Interface responsiva (via CDN) |
| HTML/CSS/JS | - | Frontend (templates Django + JS vanilla) |

## Pré-requisitos

- **Python 3.12** ou superior
- **PostgreSQL** instalado e rodando
- **Git**

## Instalação e Execução

### 1. Clone o repositório

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

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

**Dependências (requirements.txt):**
- `Django>=5.0,<7.0` — Framework web
- `psycopg2-binary>=2.9` — Driver PostgreSQL para Python
- `python-dotenv>=1.0` — Carregamento de variáveis de ambiente

### 4. Configure as variáveis de ambiente

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

### 6. Execute as migrações

```bash
python manage.py migrate
```

### 7. Crie um superusuário

```bash
python manage.py createsuperuser
```

### 8. Inicie o servidor

```bash
python manage.py runserver
```

Acesse: **http://localhost:8000**

## Testes

O projeto possui **30 testes automatizados** organizados por entidade, cobrindo models, forms, views, RBAC, privacidade, busca, paginação e endpoints JSON.

```bash
python manage.py test voos -v2
```

## Controle de Acesso

| Ação | Staff (admin) | Usuário comum |
|------|:---:|:---:|
| Ver dashboard | Sim | Sim |
| Listar aviões/voos/clientes | Sim | Sim |
| Criar/editar/excluir aviões | Sim | Não (403) |
| Criar/editar/excluir voos | Sim | Não (403) |
| Criar/editar/excluir clientes | Sim | Não (403) |
| Criar reserva | Sim | Sim |
| Ver reservas | Todas | Apenas as suas |
| Cancelar reserva | Todas | Apenas as suas |

## Arquitetura

```
voos/
├── models/                  # 1 arquivo por entidade
│   ├── aviao.py             #   UUID PK, modelo, fabricante, max_passageiros
│   ├── voo.py               #   UUID PK, FK avião, properties (assentos_disponíveis, está_lotado)
│   ├── cliente.py           #   UUID PK, FK usuário (User), email/cpf unique
│   └── reserva.py           #   UUID PK, UniqueConstraints (voo+assento, voo+cliente)
├── views/                   # 1 arquivo por entidade
│   ├── mixins.py            #   StaffRequiredMixin (RBAC)
│   ├── home.py              #   Dashboard (delega para DashboardService)
│   ├── aviao.py             #   CRUD (StaffRequired para CUD)
│   ├── voo.py               #   CRUD + busca + endpoint JSON assentos
│   ├── cliente.py           #   CRUD + busca (StaffRequired para CUD)
│   └── reserva.py           #   CRUD com filtro de privacidade
├── forms/                   # 1 arquivo por entidade
│   ├── aviao_form.py        #   Validação max_passageiros > 0
│   ├── voo_form.py          #   Widgets date/time
│   ├── cliente_form.py      #   Validação CPF 11 dígitos
│   └── reserva_form.py      #   Delega validações para ReservaService
├── services/                # Camada de serviço (lógica de negócio)
│   ├── reserva_service.py   #   Validações: assento, capacidade, cliente único
│   └── dashboard_service.py #   Cálculo de métricas (totais, ocupação, próximos voos)
├── tests/                   # 1 arquivo por entidade
│   ├── base.py              #   BaseTestCase (staff) + RegularUserTestCase
│   ├── test_aviao.py        #   Model, View, RBAC
│   ├── test_voo.py          #   Model, View, Assentos endpoint
│   ├── test_cliente.py      #   Model, View, unique constraints
│   ├── test_reserva.py      #   Model, Form, View, Privacidade
│   ├── test_dashboard.py    #   Métricas vazias e com dados
│   └── test_pagination.py   #   Paginação
├── admin.py                 # search_fields, list_filter, date_hierarchy
└── urls.py                  # UUID routes (<uuid:pk>)
```

## Modelo de Dados

```
Avião (1) ──── (N) Voo (1) ──── (N) Reserva (N) ──── (1) Cliente ──── (1) User
  id (UUID)          id (UUID)         id (UUID)           id (UUID)
  modelo             avião (FK)        voo (FK)            usuário (FK → User)
  fabricante         origem            cliente (FK)        nome
  max_passageiros    destino           número_assento      email (unique)
                     data              criado_em           cpf (unique)
                     horário                               telefone

Constraints:
  UNIQUE(voo, número_assento) — assento único por voo
  UNIQUE(voo, cliente) — um cliente por voo
```
