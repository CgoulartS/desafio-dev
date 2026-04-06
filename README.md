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
- **Interface gráfica** responsiva com Bootstrap 5 e design system customizado
- **Autenticação** com login/logout obrigatório

### Diferenciais
- **Dashboard** com métricas: totais, taxa de ocupação média, próximos voos
- **Busca e filtros**: voos por origem/destino/data, clientes por nome/email/CPF
- **Paginação** em todas as listagens (10 itens por página)
- **Seleção visual de assentos**: mapa interativo (verde = disponível, vermelho = ocupado)
- **UUID como PK**: previne ataques IDOR (sem IDs incrementais nas URLs)
- **RBAC**: permissões distintas para staff vs usuários comuns
- **LGPD**: dados pessoais de clientes acessíveis apenas por staff
- **Cache**: dashboard com cache inteligente (preparado para Redis)
- **Service layer**: lógica de negócio separada das views
- **BaseModel abstrata**: DRY com UUID + timestamps (created_at, updated_at)
- **Multi-app por domínio**: `accounts` (identidade) + `flights` (negócio) desacoplados

## Tecnologias

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Python | 3.12+ | Linguagem backend |
| Django | 6.0 | Framework web |
| PostgreSQL | 14+ | Banco de dados |
| Bootstrap | 5.3 | Interface responsiva (via CDN) |

## Pré-requisitos

- **Python 3.12** ou superior
- **PostgreSQL** instalado e rodando
- **Git**

## Instalação e Execução

```bash
git clone https://github.com/CgoulartS/desafio-dev.git
cd desafio-dev
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # edite com suas credenciais
psql -U seu-usuario -d postgres -c "CREATE DATABASE skybooker"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver     # http://localhost:8000
```

## Testes

**32 testes automatizados** — models, forms, views, RBAC, LGPD, privacidade, cache, paginação:

```bash
python manage.py test accounts flights -v2
```

## Controle de Acesso

| Ação | Staff | Usuário comum |
|------|:---:|:---:|
| Dashboard | Sim | Sim |
| Listar aviões/voos | Sim | Sim |
| Criar/editar/excluir aviões/voos | Sim | Não (403) |
| **Gerenciar clientes** | **Sim** | **Não (403) — LGPD** |
| Criar reserva | Sim | Sim |
| Ver reservas | Todas | Apenas suas |
| Cancelar reserva | Todas | Apenas suas |

## Decisões Arquiteturais

### Por que Multi-App e não Clean Architecture/DDD?

O projeto usa **duas apps Django separadas por domínio**:

- **`accounts/`** — Identidade (Cliente → User)
- **`flights/`** — Negócio (Avião, Voo, Reserva)

**Dependência:** `flights` → `accounts` (nunca o contrário).

Clean Architecture, Hexagonal e DDD são válidos para sistemas maiores. Para 4 entidades Django, a separação em apps por domínio + service layer oferece o equilíbrio ideal entre organização e pragmatismo. O Django ORM já funciona como repository pattern, e os services isolam a lógica de negócio.

Detalhes: [`docs/architecture-decision-record.md`](docs/architecture-decision-record.md)

### BaseModel DRY (ADR-002)

Todos os models herdam de `core.BaseModel` — UUID PK + `created_at` + `updated_at`, zero repetição.

### LGPD (ADR-003)

Dados pessoais protegidos. Usuários comuns não acessam lista de clientes.

### Cache (ADR-004)

Dashboard com cache (TTL 60s). LocMemCache para dev, preparado para Redis em produção.

## Arquitetura

```
desafio-dev/
├── core/                        # BaseModel abstrata (UUID + timestamps)
├── accounts/                    # Domínio: Identidade (LGPD)
│   ├── models.py                # Cliente (→ BaseModel, FK → User)
│   ├── views/                   # StaffRequired (LGPD)
│   ├── forms/                   # Validação CPF
│   └── tests/                   # LGPD tests
├── flights/                     # Domínio: Negócio
│   ├── models/                  # Avião, Voo, Reserva (→ BaseModel)
│   ├── views/                   # CRUD + RBAC + busca + assentos JSON
│   ├── forms/                   # Validações delegadas ao Service
│   ├── services/                # ReservaService + DashboardService (cache)
│   └── tests/                   # RBAC, privacidade, cache, paginação
├── templates/
│   ├── accounts/                # Staff-only
│   └── flights/                 # Público autenticado
└── static/css/style.css         # Design system
```

## Modelo de Dados

```
core.BaseModel (abstract) ── id(UUID) + created_at + updated_at

accounts.Cliente             flights.Avião
  → usuario (FK User)          → modelo, fabricante, max_passageiros
  → nome, email, cpf, tel

flights.Voo                  flights.Reserva
  → avião (FK)                 → cliente (FK accounts.Cliente)
  → origem, destino            → voo (FK)
  → data, horário              → numero_assento
                               UNIQUE(voo, assento) + UNIQUE(voo, cliente)
```
