# SkyBooker - Sistema de Reservas de Voos - Product Requirements Document (PRD)

## Goals and Background Context

### Goals

- Desenvolver uma aplicacao web completa para gerenciamento de reservas de voos
- Implementar operacoes CRUD para avioes, voos, clientes e reservas
- Garantir integridade de dados (assentos unicos, capacidade maxima)
- Disponibilizar codigo no GitHub com instrucoes de uso e dependencias
- Entregar interface grafica funcional com autenticacao (bonus)

### Background Context

Uma empresa foi contratada para criar um sistema de registro de reservas de voos. O sistema precisa gerenciar o ciclo completo: cadastro de avioes com capacidade maxima de passageiros, criacao de voos vinculados a avioes existentes, registro de clientes e associacao destes a voos especificos com assentos unicos.

Este e um desafio tecnico academico que exige demonstracao de competencia em Django + PostgreSQL, com foco em operacoes CRUD, integridade referencial e regras de negocio de dominio aereo simplificado.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2026-04-06 | 1.0 | PRD inicial criado | Morgan (PM) |

---

## Requirements

### Functional

- **FR-1:** O sistema deve permitir cadastrar avioes com modelo, fabricante e numero maximo de passageiros
- **FR-2:** O sistema deve permitir listar, editar e excluir avioes cadastrados
- **FR-3:** O sistema deve permitir criar voos associados a avioes existentes, com origem, destino, data e horario
- **FR-4:** O sistema deve permitir listar todos os voos disponiveis com detalhes completos (aviao, origem, destino, data, horario)
- **FR-5:** O sistema deve permitir editar e excluir voos cadastrados
- **FR-6:** O sistema deve permitir cadastrar clientes com nome, email, CPF e telefone
- **FR-7:** O sistema deve permitir listar, editar e excluir clientes cadastrados
- **FR-8:** O sistema deve permitir registrar reservas associando um cliente a um voo especifico com numero de assento unico
- **FR-9:** O sistema deve impedir reservas com numero de assento duplicado no mesmo voo (UNIQUE: voo + assento)
- **FR-10:** O sistema deve impedir que o numero de reservas de um voo exceda a capacidade maxima do aviao
- **FR-11:** O sistema deve permitir listar, editar e cancelar (excluir) reservas
- **FR-12:** O sistema deve exigir autenticacao (login/logout) para acessar todas as funcionalidades (bonus)
- **FR-13:** O sistema deve fornecer interface grafica web para todas as operacoes (bonus)

### Non Functional

- **NFR-1:** O sistema deve usar Django 5.x como framework backend
- **NFR-2:** O sistema deve usar PostgreSQL como banco de dados
- **NFR-3:** O codigo deve estar disponivel no GitHub com README contendo instrucoes de uso e dependencias
- **NFR-4:** O sistema deve validar dados de entrada em todos os formularios (campos obrigatorios, formatos)
- **NFR-5:** O sistema deve usar Django ORM para todas as operacoes de banco de dados (sem SQL raw)
- **NFR-6:** O sistema deve ter interface responsiva (Bootstrap 5)

---

## User Interface Design Goals

### Overall UX Vision

Interface web simples, funcional e intuitiva. Foco em usabilidade para operacoes CRUD rapidas. Navegacao clara entre as 4 entidades principais (avioes, voos, clientes, reservas) com feedback visual para acoes do usuario (mensagens de sucesso/erro).

### Key Interaction Paradigms

- Navegacao por menu/navbar fixo com links para cada entidade
- Tabelas de listagem com acoes inline (editar, excluir)
- Formularios modais ou paginas dedicadas para criacao/edicao
- Confirmacao antes de exclusao (pagina de confirmacao)
- Mensagens flash do Django para feedback de operacoes

### Core Screens and Views

1. **Login** - Tela de autenticacao
2. **Dashboard/Home** - Redirect para lista de voos (entidade principal)
3. **Lista de Avioes** - Tabela com modelo, fabricante, capacidade + acoes CRUD
4. **Formulario de Aviao** - Cadastro/edicao de aviao
5. **Lista de Voos** - Tabela com aviao, origem, destino, data, horario + acoes CRUD
6. **Detalhes do Voo** - Informacoes do voo + lista de passageiros/reservas
7. **Formulario de Voo** - Cadastro/edicao de voo (select de aviao)
8. **Lista de Clientes** - Tabela com nome, email, CPF, telefone + acoes CRUD
9. **Formulario de Cliente** - Cadastro/edicao de cliente
10. **Lista de Reservas** - Tabela com cliente, voo, assento + acoes CRUD
11. **Formulario de Reserva** - Cadastro/edicao com selects de cliente e voo + campo de assento

### Accessibility

None (nao e requisito do desafio)

### Branding

Sem branding especifico. Usar Bootstrap 5 default com tema limpo. Cores neutras.

### Target Device and Platforms

Web Responsive (Bootstrap 5 via CDN)

---

## Technical Assumptions

### Repository Structure

**Monorepo** - Um unico repositorio `desafio-dev` contendo o projeto Django completo.

### Service Architecture

**Monolith Django** - Uma unica aplicacao Django com uma app `voos` contendo todos os models, views e templates. Justificativa: complexidade SIMPLE (score 8/25), nao justifica separacao em multiplas apps ou servicos.

### Testing Requirements

**Unit + Integration** - Testes unitarios para models (validacoes, constraints) e testes de integracao para views (CRUD operations, autenticacao). Framework: `django.test.TestCase`.

### Additional Technical Assumptions and Requests

- **Stack:** Django 5.x + PostgreSQL 16 + Bootstrap 5 (CDN)
- **Python:** 3.12+
- **ORM:** Django ORM nativo (sem SQLAlchemy ou raw SQL)
- **Autenticacao:** `django.contrib.auth` built-in
- **Views:** Class-Based Views (ListView, CreateView, UpdateView, DeleteView, DetailView)
- **Forms:** Django ModelForms com validacao customizada
- **Config:** python-dotenv para variaveis de ambiente (.env)
- **Dependencias:** Django, psycopg2-binary, python-dotenv
- **Deploy:** Local development (manage.py runserver)
- **Migrations:** Django migrations automaticas

---

## Epic List

### Epic 1: Fundacao do Projeto e CRUD de Avioes

Estabelecer a infraestrutura do projeto Django com PostgreSQL, configurar autenticacao e implementar o primeiro CRUD completo (Avioes) com interface grafica.

### Epic 2: CRUD de Voos, Clientes e Reservas

Implementar os CRUDs restantes (Voos, Clientes, Reservas) com todas as regras de negocio, validacoes e testes. Finalizar documentacao.

**Rationale:** Dois epics sao suficientes para este escopo SIMPLE. O Epic 1 entrega valor imediato (projeto funcional com primeiro CRUD + auth). O Epic 2 completa o sistema com as demais entidades e regras de negocio.

---

## Epic 1: Fundacao do Projeto e CRUD de Avioes

**Goal:** Entregar o projeto Django funcional com PostgreSQL configurado, autenticacao implementada e CRUD completo de Avioes com interface grafica. Ao final deste epic, o sistema estara rodando com login obrigatorio e gerenciamento de avioes funcional.

### Story 1.1: Setup do Projeto Django com PostgreSQL

> Como desenvolvedor,
> eu quero um projeto Django configurado com PostgreSQL e estrutura base,
> para que eu tenha a fundacao pronta para implementar as funcionalidades.

**Acceptance Criteria:**

1. Projeto Django criado com app `voos` registrada em INSTALLED_APPS
2. `settings.py` configurado para usar PostgreSQL via variaveis de ambiente (.env)
3. `requirements.txt` com Django, psycopg2-binary, python-dotenv
4. `.env.example` com template das variaveis necessarias (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, SECRET_KEY)
5. Template base (`base.html`) com Bootstrap 5 via CDN, navbar e bloco de conteudo
6. Pagina inicial (home) acessivel em `/`
7. `README.md` com instrucoes de setup (clonar, criar venv, instalar deps, configurar .env, migrate, runserver)
8. `python manage.py check` executa sem erros
9. Migrations iniciais aplicadas com sucesso

### Story 1.2: Autenticacao (Login/Logout)

> Como usuario do sistema,
> eu quero fazer login e logout,
> para que apenas usuarios autenticados acessem o sistema.

**Acceptance Criteria:**

1. Paginas de login (`/login/`) e logout (`/logout/`) funcionais
2. Templates de login e logout com layout Bootstrap (usando `base.html`)
3. Redirect para `/login/` quando usuario nao autenticado tenta acessar qualquer pagina
4. Redirect para home (`/`) apos login bem-sucedido
5. Link de logout visivel na navbar quando autenticado
6. Comando para criar superuser documentado no README
7. `LoginRequiredMixin` aplicado como padrao para todas as views

### Story 1.3: CRUD Completo de Avioes

> Como usuario do sistema,
> eu quero cadastrar, listar, editar e excluir avioes,
> para que eu possa gerenciar a frota disponivel para voos.

**Acceptance Criteria:**

1. Model `Aviao` com campos: modelo (CharField), fabricante (CharField), max_passageiros (PositiveIntegerField)
2. ListView em `/avioes/` exibindo tabela com todos os avioes e acoes (editar, excluir)
3. CreateView em `/avioes/novo/` com formulario validado
4. UpdateView em `/avioes/<id>/editar/` com formulario pre-preenchido
5. DeleteView em `/avioes/<id>/excluir/` com pagina de confirmacao
6. Validacao: max_passageiros deve ser maior que 0
7. Mensagens flash de sucesso apos criar, editar e excluir
8. Todas as views protegidas por `LoginRequiredMixin`
9. Links de navegacao na navbar para lista de avioes
10. Testes unitarios para model e testes de integracao para views (min. 5 testes)

---

## Epic 2: CRUD de Voos, Clientes e Reservas

**Goal:** Completar o sistema com CRUD de Voos, Clientes e Reservas, implementando todas as regras de negocio (capacidade maxima, assento unico), validacoes e testes. Ao final, o sistema estara completo e documentado.

### Story 2.1: CRUD Completo de Voos

> Como usuario do sistema,
> eu quero cadastrar, listar, visualizar detalhes, editar e excluir voos,
> para que eu possa gerenciar os voos disponiveis para reserva.

**Acceptance Criteria:**

1. Model `Voo` com campos: aviao (ForeignKey para Aviao), origem (CharField), destino (CharField), data (DateField), horario (TimeField)
2. ListView em `/voos/` exibindo tabela com aviao, origem, destino, data, horario e acoes
3. DetailView em `/voos/<id>/` mostrando detalhes do voo e lista de reservas/passageiros
4. CreateView em `/voos/novo/` com select de avioes existentes
5. UpdateView em `/voos/<id>/editar/`
6. DeleteView em `/voos/<id>/excluir/` com confirmacao
7. Validacao: aviao deve existir (integridade referencial)
8. Mensagens flash de sucesso para todas as operacoes
9. Todas as views protegidas por `LoginRequiredMixin`
10. Testes unitarios e de integracao (min. 5 testes)

### Story 2.2: CRUD Completo de Clientes

> Como usuario do sistema,
> eu quero cadastrar, listar, editar e excluir clientes,
> para que eu possa gerenciar os passageiros que farao reservas.

**Acceptance Criteria:**

1. Model `Cliente` com campos: nome (CharField), email (EmailField), cpf (CharField com max_length=11), telefone (CharField)
2. ListView em `/clientes/` exibindo tabela com nome, email, CPF, telefone e acoes
3. CreateView em `/clientes/novo/`
4. UpdateView em `/clientes/<id>/editar/`
5. DeleteView em `/clientes/<id>/excluir/` com confirmacao
6. Validacao: email unico, CPF unico (unique=True)
7. Mensagens flash de sucesso para todas as operacoes
8. Todas as views protegidas por `LoginRequiredMixin`
9. Testes unitarios e de integracao (min. 5 testes)

### Story 2.3: CRUD de Reservas com Regras de Negocio

> Como usuario do sistema,
> eu quero criar, listar, editar e cancelar reservas associando clientes a voos com assentos unicos,
> para que cada passageiro tenha um assento garantido sem conflitos.

**Acceptance Criteria:**

1. Model `Reserva` com campos: cliente (ForeignKey), voo (ForeignKey), numero_assento (PositiveIntegerField), criado_em (DateTimeField auto)
2. Constraint UNIQUE em (voo, numero_assento) — assento unico por voo
3. Constraint UNIQUE em (voo, cliente) — um cliente por voo
4. Validacao no form/model: numero_assento nao pode exceder max_passageiros do aviao do voo
5. Validacao no form/model: numero total de reservas do voo nao pode exceder max_passageiros
6. ListView em `/reservas/` exibindo tabela com cliente, voo, assento e acoes
7. CreateView em `/reservas/nova/` com selects de cliente e voo + campo de assento
8. UpdateView em `/reservas/<id>/editar/`
9. DeleteView em `/reservas/<id>/excluir/` com confirmacao
10. Mensagens de erro claras quando validacoes falham (assento ocupado, voo lotado)
11. Mensagens flash de sucesso para todas as operacoes
12. Todas as views protegidas por `LoginRequiredMixin`
13. Testes unitarios e de integracao cobrindo regras de negocio (min. 8 testes)

### Story 2.4: Finalizacao e Documentacao

> Como avaliador do desafio,
> eu quero documentacao clara de como instalar e usar o sistema,
> para que eu possa avaliar o projeto sem dificuldades.

**Acceptance Criteria:**

1. `README.md` atualizado com: descricao do projeto, tecnologias usadas, pre-requisitos, instrucoes passo-a-passo de instalacao, como rodar, como criar superuser, como rodar testes
2. `.env.example` completo e atualizado com todas as variaveis
3. Admin do Django configurado com registro de todos os 4 models
4. Todos os testes passando (`python manage.py test`)
5. Nenhum erro de migracao (`python manage.py migrate --check`)

---

## Next Steps

### UX Expert Prompt

> @ux-design-expert: Revise o PRD (docs/prd.md) e crie os wireframes/layouts para as 11 telas identificadas, usando Bootstrap 5. Foco em usabilidade para CRUD rapido com tabelas, formularios e navegacao por navbar.

### Architect Prompt

> @architect: Revise o PRD (docs/prd.md) e crie a arquitetura completa do sistema usando `*create-full-stack-architecture`. Stack definido: Django 5.x + PostgreSQL + Bootstrap 5 CDN. Monolith com app unica `voos`. CBVs para CRUD. Autenticacao com django.contrib.auth.
