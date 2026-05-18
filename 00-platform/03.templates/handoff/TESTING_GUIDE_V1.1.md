# GUÍA DE TESTING

**Documento:** TESTING_GUIDE.md  
**Versión:** 1.1  
**Fecha:** 2026-03-30  
**Autor:** PJM-Agent  
**Aplica a:** Todos los proyectos con equipo de agentes  
**Estado:** 📋 ESTÁNDAR OBLIGATORIO

---

## 0. PROPÓSITO

Esta guía define el proceso estándar de Testing para equipos de agentes virtuales. Es un documento **cross-sprint** que explica **cómo** hacer testing — los handoffs de cada sprint definen **qué** escenarios testear específicamente.

> **Regla fundamental:** Testing es OBLIGATORIO en cada sprint. No es actividad opcional ni "si hay tiempo".

---

## 1. ESTRATEGIA DE TESTING

### 1.1 Pirámide de Tests

```
            ┌─────────────┐
            │     E2E     │  ← Flujos críticos completos (10%)
            │             │     Más lentos, más frágiles
            ├─────────────┤
            │ Integration │  ← Endpoints + DB (30%)
            │             │     Verifican contratos
            ├─────────────┤
            │    Unit     │  ← Services + componentes (60%)
            │             │     Rápidos, aislados
            └─────────────┘
```

### 1.2 Cobertura Mínima por Capa

| Capa | Stack | Cobertura mínima | Herramienta típica |
|------|-------|------------------|-------------------|
| Unit BE | Node/Express | ≥ 70% | Jest |
| Unit BE | Python/FastAPI | ≥ 70% | pytest |
| Unit FE | React/Vue | ≥ 60% | Jest/Vitest |
| Integration | API | 100% endpoints | Supertest/pytest |
| E2E | Full stack | 100% flujos críticos | Playwright/Cypress |

### 1.3 Responsabilidades

| Rol | Responsabilidad de testing |
|-----|---------------------------|
| **BE** | Unit tests de services, integration tests de endpoints |
| **FE** | Unit tests de componentes, integration tests de páginas |
| **QA** | E2E tests, regression tests, test plan |
| **TL** | Verificar cobertura, revisar tests en Code Review |

---

## 2. TESTS UNITARIOS — BACKEND

### 2.1 Estructura de Archivos

```
/tests/
├── unit/
│   ├── services/
│   │   ├── [service_name].test.ts    # Node
│   │   └── test_[service_name].py    # Python
│   ├── utils/
│   └── validators/
├── integration/
│   └── [module]/
└── e2e/
    └── flows/
```

### 2.2 Convenciones de Naming

| Stack | Convención | Ejemplo |
|-------|-----------|---------|
| Node/Jest | `[file].test.ts` | `user.service.test.ts` |
| Python/pytest | `test_[file].py` | `test_user_service.py` |

### 2.3 Anatomía de un Test Unitario

```typescript
// Node/Jest example
describe('UserService', () => {
  // Setup
  let service: UserService;
  let mockRepository: jest.Mocked<UserRepository>;
  
  beforeEach(() => {
    mockRepository = createMockRepository();
    service = new UserService(mockRepository);
  });
  
  // Grupo por método
  describe('createUser', () => {
    // Test case con patrón Given-When-Then
    it('should create user with valid data', async () => {
      // Given (Arrange)
      const userData = { email: 'test@test.com', name: 'Test' };
      mockRepository.create.mockResolvedValue({ id: '1', ...userData });
      
      // When (Act)
      const result = await service.createUser(userData);
      
      // Then (Assert)
      expect(result).toHaveProperty('id');
      expect(mockRepository.create).toHaveBeenCalledWith(userData);
    });
    
    it('should reject duplicate email', async () => {
      // Given
      mockRepository.findByEmail.mockResolvedValue({ id: '1' });
      
      // When/Then
      await expect(service.createUser({ email: 'existing@test.com' }))
        .rejects.toThrow('Email already exists');
    });
  });
});
```

```python
# Python/pytest example
class TestUserService:
    @pytest.fixture
    def service(self, mock_repository):
        return UserService(repository=mock_repository)
    
    @pytest.fixture
    def mock_repository(self, mocker):
        return mocker.Mock(spec=UserRepository)
    
    def test_create_user_valid_data(self, service, mock_repository):
        """Should create user with valid data"""
        # Given
        user_data = {"email": "test@test.com", "name": "Test"}
        mock_repository.create.return_value = {"id": "1", **user_data}
        
        # When
        result = service.create_user(user_data)
        
        # Then
        assert "id" in result
        mock_repository.create.assert_called_once_with(user_data)
    
    def test_create_user_duplicate_email(self, service, mock_repository):
        """Should reject duplicate email"""
        # Given
        mock_repository.find_by_email.return_value = {"id": "1"}
        
        # When/Then
        with pytest.raises(DuplicateEmailError):
            service.create_user({"email": "existing@test.com"})
```

### 2.4 Checklist de Unit Test BE

```markdown
## Unit Test Checklist — Backend

### Cobertura
- [ ] Happy path testeado
- [ ] Edge cases testeados
- [ ] Error cases testeados
- [ ] Validaciones testeadas

### Calidad
- [ ] Tests aislados (no dependen de otros tests)
- [ ] Mocks correctamente configurados
- [ ] Assertions específicas (no solo "no throws")
- [ ] Nombres descriptivos

### Mantenibilidad
- [ ] Setup compartido en beforeEach/fixtures
- [ ] No hay datos hardcodeados (usar factories)
- [ ] Tests rápidos (< 100ms cada uno)
```

---

## 3. TESTS UNITARIOS — FRONTEND

### 3.1 Estructura de Archivos

```
/src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx       # Test del componente
│   │   └── Button.stories.tsx    # Storybook (opcional)
│   └── ...
├── features/
│   └── [feature]/
│       ├── components/
│       ├── hooks/
│       │   ├── useFeature.ts
│       │   └── useFeature.test.ts
│       └── ...
└── __tests__/
    └── integration/
```

### 3.2 Testing de Componentes

```tsx
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with label', () => {
    render(<Button>Click me</Button>);
    
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });
  
  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    
    fireEvent.click(screen.getByRole('button'));
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
  
  it('shows loading state', () => {
    render(<Button loading>Submit</Button>);
    
    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByTestId('spinner')).toBeInTheDocument();
  });
  
  it('applies variant styles', () => {
    render(<Button variant="primary">Primary</Button>);
    
    expect(screen.getByRole('button')).toHaveClass('btn-primary');
  });
});
```

### 3.3 Testing de Hooks

```tsx
// useCounter.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    
    expect(result.current.count).toBe(0);
  });
  
  it('initializes with custom value', () => {
    const { result } = renderHook(() => useCounter(10));
    
    expect(result.current.count).toBe(10);
  });
  
  it('increments count', () => {
    const { result } = renderHook(() => useCounter());
    
    act(() => {
      result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
  });
});
```

### 3.4 Checklist de Unit Test FE

```markdown
## Unit Test Checklist — Frontend

### Componentes
- [ ] Render inicial testeado
- [ ] Props variantes testeadas
- [ ] Estados testeados (loading, error, success)
- [ ] Interacciones testeadas (click, input, submit)
- [ ] Accesibilidad verificada (roles, labels)

### Hooks
- [ ] Valor inicial testeado
- [ ] Actualizaciones de estado testeadas
- [ ] Side effects testeados (con mocks)
- [ ] Cleanup testeado (useEffect return)

### Calidad
- [ ] Usa Testing Library queries correctas (getByRole > getByTestId)
- [ ] No testa implementación interna
- [ ] Tests representan uso real del usuario
```

---

## 4. TESTS DE INTEGRACIÓN

### 4.1 Definición

Los tests de integración verifican que **múltiples componentes funcionan juntos correctamente**. Para APIs, esto significa probar el endpoint completo: routing → controller → service → database.

### 4.2 Setup de Base de Datos

```typescript
// Node/Jest with test database
import { TestDatabase } from '../utils/test-db';

describe('User API', () => {
  let db: TestDatabase;
  
  beforeAll(async () => {
    db = await TestDatabase.create();
  });
  
  afterAll(async () => {
    await db.destroy();
  });
  
  beforeEach(async () => {
    await db.reset(); // Truncate all tables
  });
  
  // Tests here...
});
```

```python
# Python/pytest with test database
@pytest.fixture(scope="session")
def db_session():
    """Create test database session"""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture(autouse=True)
def reset_db(db_session):
    """Reset database before each test"""
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()
```

### 4.3 Anatomía de Test de Integración

```typescript
// Node/Supertest
import request from 'supertest';
import { app } from '../app';

describe('POST /api/users', () => {
  it('creates user and returns 201', async () => {
    // Given
    const userData = { email: 'new@test.com', name: 'New User' };
    
    // When
    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .set('Authorization', `Bearer ${validToken}`);
    
    // Then
    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
    expect(response.body.email).toBe(userData.email);
    
    // Verify in database
    const dbUser = await db.query('SELECT * FROM users WHERE id = $1', [response.body.id]);
    expect(dbUser.rows[0].email).toBe(userData.email);
  });
  
  it('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'invalid', name: 'Test' })
      .set('Authorization', `Bearer ${validToken}`);
    
    expect(response.status).toBe(400);
    expect(response.body.error).toContain('email');
  });
  
  it('returns 401 without auth token', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@test.com', name: 'Test' });
    
    expect(response.status).toBe(401);
  });
});
```

### 4.4 Checklist de Integration Test

```markdown
## Integration Test Checklist

### Por Endpoint
- [ ] Happy path con datos válidos
- [ ] Validación de request (400)
- [ ] Autenticación requerida (401)
- [ ] Autorización correcta (403)
- [ ] Recurso no encontrado (404)
- [ ] Conflictos/duplicados (409)
- [ ] Error interno manejado (500)

### Base de Datos
- [ ] Datos persistidos correctamente
- [ ] Relaciones creadas correctamente
- [ ] Constraints respetados
- [ ] Transacciones funcionan

### Integración
- [ ] Headers correctos en response
- [ ] Formato de respuesta estándar
- [ ] Paginación funciona (si aplica)
```

---

## 5. TESTS END-TO-END (E2E)

### 5.1 Definición

Los tests E2E verifican **flujos completos desde la perspectiva del usuario**, incluyendo frontend, backend, y servicios externos.

### 5.2 Flujos Críticos a Testear

Los flujos críticos son aquellos que, si fallan, **impiden el uso del sistema**:

| Categoría | Ejemplos de flujos críticos |
|-----------|---------------------------|
| **Auth** | Login, logout, refresh token |
| **Core business** | Crear/editar/eliminar entidades principales |
| **Pagos** | Checkout completo, cancelación |
| **Onboarding** | Registro, setup inicial |

### 5.3 Anatomía de Test E2E

```typescript
// Playwright example
import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {
  test('complete registration successfully', async ({ page }) => {
    // Navigate
    await page.goto('/register');
    
    // Fill form
    await page.fill('[data-testid="email-input"]', 'new@test.com');
    await page.fill('[data-testid="password-input"]', 'SecurePass123!');
    await page.fill('[data-testid="name-input"]', 'New User');
    
    // Submit
    await page.click('[data-testid="submit-button"]');
    
    // Verify redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    
    // Verify welcome message
    await expect(page.locator('[data-testid="welcome-message"]'))
      .toContainText('Welcome, New User');
  });
  
  test('shows error for existing email', async ({ page }) => {
    // Pre-condition: user already exists
    await page.goto('/register');
    
    await page.fill('[data-testid="email-input"]', 'existing@test.com');
    await page.fill('[data-testid="password-input"]', 'SecurePass123!');
    await page.fill('[data-testid="name-input"]', 'Existing');
    
    await page.click('[data-testid="submit-button"]');
    
    // Verify error shown
    await expect(page.locator('[data-testid="error-message"]'))
      .toContainText('Email already registered');
    
    // Verify still on register page
    await expect(page).toHaveURL('/register');
  });
});
```

### 5.4 QA-FLOW Scenarios

Para cada sprint, QA define escenarios de flujo específicos:

```markdown
## QA-FLOW Scenarios — Sprint [N]

### QA-FLOW-01: [Nombre del flujo]
**Precondiciones:** [Estado inicial requerido]
**Pasos:**
1. [Acción 1]
2. [Acción 2]
3. [Acción 3]
**Resultado esperado:** [Qué debe pasar]
**Verificaciones adicionales:**
- [ ] [Check 1]
- [ ] [Check 2]

### QA-FLOW-02: [Nombre del flujo]
...
```

> **Nota QA-FLOW-05:** Siempre se coordina con DL-REVIEW.
> DL valida visualmente (impl vs HTMLs), QA valida navegación funcional.
> Ejecutar en paralelo — no son redundantes.

### 5.5 Checklist de E2E Test

```markdown
## E2E Test Checklist

### Flujo
- [ ] Flujo completo funciona
- [ ] Estados intermedios correctos
- [ ] Navegación correcta
- [ ] Datos persisten entre páginas

### UI
- [ ] Loading states visibles
- [ ] Error messages claros
- [ ] Success feedback presente
- [ ] Responsive funciona

### Edge Cases
- [ ] Timeout de API manejado
- [ ] Sesión expirada manejada
- [ ] Errores de red manejados
```

---

## 6. MOCKING STRATEGY

### 6.1 Qué Mockear y Qué No

| Capa | Unit Tests | Integration Tests | E2E Tests |
|------|-----------|-------------------|-----------|
| **Base de datos** | ✅ Mock | ❌ Real (test DB) | ❌ Real (test DB) |
| **APIs externas** | ✅ Mock | ✅ Mock | ⚠️ Depends |
| **File system** | ✅ Mock | ⚠️ Depends | ❌ Real |
| **Time/Date** | ✅ Mock | ✅ Mock | ⚠️ Depends |
| **Random** | ✅ Mock (seed) | ✅ Mock (seed) | ⚠️ Depends |

### 6.2 Mocking de APIs Externas

```typescript
// Node/Jest - Mock de servicio externo
jest.mock('../services/external-api', () => ({
  ExternalAPI: {
    fetchData: jest.fn().mockResolvedValue({
      status: 'success',
      data: { id: 1, value: 'mocked' }
    })
  }
}));

// Para tests específicos
beforeEach(() => {
  (ExternalAPI.fetchData as jest.Mock).mockClear();
});

it('handles external API error', async () => {
  (ExternalAPI.fetchData as jest.Mock).mockRejectedValueOnce(
    new Error('API unavailable')
  );
  
  // Test error handling...
});
```

### 6.3 Fixtures y Factories

```typescript
// factories/user.factory.ts
import { faker } from '@faker-js/faker';

export const createUser = (overrides = {}) => ({
  id: faker.datatype.uuid(),
  email: faker.internet.email(),
  name: faker.person.fullName(),
  createdAt: faker.date.past(),
  ...overrides
});

// Usage in tests
const user = createUser({ email: 'specific@test.com' });
```

```python
# Python with factory_boy
import factory
from faker import Faker

fake = Faker()

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    id = factory.LazyFunction(lambda: str(uuid4()))
    email = factory.LazyFunction(lambda: fake.email())
    name = factory.LazyFunction(lambda: fake.name())

# Usage
user = UserFactory(email="specific@test.com")
```

---

## 7. CI/CD GATES

### 7.1 Pipeline Gates

| Gate | Umbral | Bloquea |
|------|--------|---------|
| Unit tests passing | 100% | ✅ Merge |
| Integration tests passing | 100% | ✅ Merge |
| Coverage BE | ≥ 70% | ✅ Merge |
| Coverage FE | ≥ 60% | ✅ Merge |
| Linting | 0 errors | ✅ Merge |
| E2E critical | 100% | ✅ Deploy |

### 7.2 Configuración de CI

```yaml
# .github/workflows/tests.yml
name: Tests

on:
  pull_request:
    branches: [main, develop]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm run test:unit -- --coverage
      
      - name: Check coverage
        run: |
          COVERAGE=$(npm run test:coverage -- --json | jq '.total.lines.pct')
          if (( $(echo "$COVERAGE < 70" | bc -l) )); then
            echo "Coverage below 70%: $COVERAGE"
            exit 1
          fi

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v3
      
      - name: Run migrations
        run: npm run db:migrate:test
      
      - name: Run integration tests
        run: npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    needs: [unit-tests, integration-tests]
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Playwright
        run: npx playwright install --with-deps
      
      - name: Run E2E tests
        run: npm run test:e2e
```

---

## 8. PROCESO DE BUGS

### 8.1 Flujo de Bug Encontrado

```
QA encuentra bug durante testing
        │
        ▼
POST /api/tasks/{taskId}/issues   ← tarea pasa a on_hold AUTOMÁTICAMENTE
        │
        ▼
TL crea FIX task → asigna a desarrollador
        │
        ▼
Developer corrige + agrega test de regresión
        │
        ▼
TL revisa fix → FIX task a task_completed
        │
        ▼
PUT /api/issues/{id} {"isResolved": true}  ← TL ejecuta esto, NO QA
        │
        ▼
Tarea vuelve a previousStatus automáticamente
```

> **⚠️ NUNCA:** QA no debe cambiar estado a `on_hold` manualmente (PATCH /status).
> El sistema lo hace solo al crear el issue. Hacerlo manual deja `previousStatus=null`
> y rompe el flujo de restauración.

### 8.2 Test de Regresión Obligatorio

Por cada bug corregido, se debe agregar un test que:
1. Reproduce el bug (falla sin el fix)
2. Pasa con el fix aplicado

```typescript
// regression/BUG-123.test.ts
describe('BUG-123: User creation fails with special characters', () => {
  it('should handle special characters in name', async () => {
    // This test was added after BUG-123 was fixed
    // It ensures the bug doesn't reappear
    
    const userData = { 
      email: 'test@test.com', 
      name: "O'Brien-Smith" // Special characters that caused the bug
    };
    
    const result = await userService.createUser(userData);
    
    expect(result.name).toBe("O'Brien-Smith");
  });
});
```

---

## 9. PRE-MERGE CHECKLIST

### 9.1 Checklist Backend

```markdown
## Pre-Merge Checklist — Backend

### Tests
- [ ] Unit tests escritos para nuevo código
- [ ] Unit tests pasan localmente
- [ ] Integration tests escritos para nuevos endpoints
- [ ] Integration tests pasan localmente
- [ ] Cobertura ≥ 70%

### Calidad
- [ ] Sin errores de linting
- [ ] Sin warnings de tipos
- [ ] Docstrings en funciones públicas
- [ ] .LOGIC.md actualizado (por cada archivo creado/modificado)

### CI
- [ ] Pipeline verde en PR
- [ ] Sin tests skipped sin razón
```

### 9.2 Checklist Frontend

```markdown
## Pre-Merge Checklist — Frontend

### Tests
- [ ] Tests de componentes escritos
- [ ] Tests pasan localmente
- [ ] Cobertura ≥ 60%

### Calidad
- [ ] Sin errores de ESLint
- [ ] Sin errores de TypeScript
- [ ] Componentes accesibles (a11y)
- [ ] .LOGIC.md actualizado (por cada archivo creado/modificado)

### CI
- [ ] Pipeline verde en PR
```

---

## 10. COMANDOS DE REFERENCIA

### 10.1 Node/Jest

```bash
# Unit tests
npm run test:unit

# Unit tests con watch
npm run test:unit -- --watch

# Coverage
npm run test:unit -- --coverage

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# Todo con coverage
npm run test -- --coverage --coverageThreshold='{"global":{"lines":70}}'
```

### 10.2 Python/pytest

```bash
# Unit tests
pytest tests/unit/ -v

# Con coverage
pytest tests/unit/ --cov=src --cov-report=term-missing

# Integration tests
pytest tests/integration/ -v

# Con markers
pytest -m "sprint10" -v

# Fail under threshold
pytest --cov=src --cov-fail-under=70
```

### 10.3 Frontend (Vitest/Jest)

```bash
# Tests de componentes
npm run test

# Con coverage
npm run test -- --coverage

# Específico archivo
npm run test -- Button.test.tsx

# Watch mode
npm run test -- --watch
```

---

## 11. APÉNDICE: TEMPLATE DE TEST PLAN

```markdown
# Test Plan — Sprint [N]

**Proyecto:** [Nombre]  
**Sprint:** [N]  
**QA:** [Nombre]  
**Fecha:** YYYY-MM-DD

---

## 1. Alcance

### In Scope
- [Lista de features a testear]

### Out of Scope
- [Features excluidas de este sprint]

---

## 2. Estrategia

| Tipo | Responsable | Herramienta | Cobertura target |
|------|-------------|-------------|------------------|
| Unit BE | BE | Jest/pytest | ≥ 70% |
| Unit FE | FE | Jest/Vitest | ≥ 60% |
| Integration | BE | Supertest | 100% endpoints |
| E2E | QA | Playwright | Flujos críticos |

---

## 3. Escenarios de Test

### 3.1 Unit Tests BE
| Service | Tests requeridos |
|---------|-----------------|
| [ServiceA] | [lista] |

### 3.2 Unit Tests FE
| Componente | Tests requeridos |
|------------|-----------------|
| [ComponentA] | [lista] |

### 3.3 Integration Tests
| Endpoint | Casos |
|----------|-------|
| POST /api/[x] | happy path, validation, auth |

### 3.4 E2E Flows
| ID | Flow | Prioridad |
|----|------|-----------|
| QA-FLOW-01 | [Descripción] | Critical |

---

## 4. Criterios de Aceptación

- [ ] Cobertura BE ≥ 70%
- [ ] Cobertura FE ≥ 60%
- [ ] 0 tests fallando
- [ ] Flujos críticos E2E pasando
- [ ] Sin bugs S1/S2 abiertos

---

## 5. Riesgos

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| [Riesgo 1] | [Alto/Medio/Bajo] | [Acción] |

---

**Aprobado por:** _______________  
**Fecha:** _______________
```

---

## 12. HISTORIAL DE VERSIONES

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-03-30 | PJM-Agent | Versión inicial estandarizada |
| 1.1 | 2026-03-30 | PJM-Agent | Correcciones: flujo bug §8.1 con PUT + warning on_hold, .LOGIC.md en checklists §9, nota coordinación DL-REVIEW en §5.4 |

---

**FIN DEL DOCUMENTO**
