# ADR — Registro de Decisões Arquiteturais

## ADR-001: Separação em Módulos por Domínio

**Status:** Aprovada
**Data:** 2026-04-06

### Contexto

O projeto iniciou como monolito em uma única app Django (`voos/`) contendo todas as entidades: Avião, Voo, Cliente, Reserva. Feedback de revisão identificou acoplamento entre domínios de identidade (Cliente/Usuário) e domínio de negócio (Aviões/Voos/Reservas).

### Decisão

Separar em duas apps Django por domínio:

- **`accounts/`** — Identidade e cadastro (Cliente, User). Módulo independente.
- **`flights/`** — Core do negócio (Avião, Voo, Reserva). Referencia `accounts`, nunca o contrário.

### Justificativa

- **Baixo acoplamento**: novos módulos futuros não precisam depender de `flights` para acessar clientes
- **Coesão**: cada módulo tem uma responsabilidade clara
- **Escalabilidade**: módulos podem evoluir independentemente
- **LGPD**: módulo de identidade pode ter políticas de acesso próprias

### Alternativas Consideradas

| Opção | Prós | Contras | Decisão |
|-------|------|---------|---------|
| **Monolito (1 app)** | Simples, rápido | Acoplamento, difícil escalar | Rejeitada |
| **Multi-app Django** | Boa separação, pragmático | Não é Clean Arch pura | **Escolhida** |
| **Clean Architecture** | Máxima separação | Over-engineering para Django, curva alta | Rejeitada para este escopo |
| **Hexagonal** | Ports/Adapters flexíveis | Complexidade sem benefício real aqui | Rejeitada para este escopo |
| **DDD** | Domain puro, bounded contexts | Projeto pequeno não justifica | Rejeitada para este escopo |

### Trade-offs

Clean Architecture / Hexagonal / DDD são padrões válidos para sistemas maiores. Para um CRUD Django com 4 entidades, a separação em apps por domínio oferece o melhor equilíbrio entre organização e pragmatismo. O Django ORM já atua como repository pattern implícito, e o service layer que implementamos fornece a separação de lógica de negócio que esses padrões exigem.

---

## ADR-002: BaseModel Abstrata com Lifecycle

**Status:** Aprovada
**Data:** 2026-04-06

### Contexto

Campos `id` (UUID), `created_at` e `updated_at` repetidos em todos os models viola o princípio DRY.

### Decisão

Criar `core/models.py` com `BaseModel` abstrata que todos os models herdam.

```python
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

### Justificativa

- **DRY**: definição única de campos comuns
- **Lifecycle**: `created_at` e `updated_at` automáticos em toda entidade
- **Extensível**: adicionar campos como `is_active`, `deleted_at` (soft delete) afeta todos os models

---

## ADR-003: LGPD — Restrição de Acesso a Dados Pessoais

**Status:** Aprovada
**Data:** 2026-04-06

### Contexto

Lista de clientes (nome, email, CPF, telefone) acessível para qualquer usuário logado. Viola LGPD — dados pessoais devem ser acessíveis apenas por quem tem necessidade operacional.

### Decisão

- `ClienteListView`, `ClienteCreateView`, `ClienteUpdateView`, `ClienteDeleteView` → **Staff only**
- Usuário comum interage com clientes apenas via formulário de reserva (select no form)
- Dados pessoais de outros clientes nunca expostos para usuários comuns

### Justificativa

- **LGPD (Art. 6)**: tratamento de dados pessoais deve ter finalidade legítima
- **Princípio do menor privilégio**: acesso apenas ao necessário
- **Segurança**: reduz superfície de exposição de dados sensíveis

---

## ADR-004: Cache no Dashboard

**Status:** Aprovada
**Data:** 2026-04-06

### Contexto

Dashboard executa queries agregadas toda vez que a página é carregada. Em produção com muitos registros, isso impacta performance.

### Decisão

Implementar cache no `DashboardService` usando Django cache framework com fallback para LocMemCache (dev) e preparado para Redis (produção).

### Justificativa

- **Performance**: evita queries repetidas em dados que mudam pouco
- **Escalabilidade**: padrão pronto para Redis em produção
- **Pragmatismo**: `cache.get_or_set()` com TTL de 60 segundos é suficiente

### Configuração

```python
# Dev: LocMemCache (padrão Django, sem dependências)
# Prod: Redis
CACHES = {
    'default': {
        'BACKEND': os.getenv('CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
    }
}
```
