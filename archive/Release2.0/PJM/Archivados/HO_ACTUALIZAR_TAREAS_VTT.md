# HO: Actualizar 116 Tareas Memory Service en VTT

**Preparado por:** PJM (pjm@memory-service.vtt.ai) — rol de coordinacion
**Ejecutor:** PM (Martin Rivas) o DO — rol con permisos de ejecucion
**Validador posterior:** PJM
**Fecha:** 2026-04-21
**Origen:** HANDOFF_PJM_SPRINT_SETUP_VTT.md v3.0 (estado real post-setup VTT)
**Proyecto:** Memory Service — MEM
**Estado:** LISTO PARA EJECUTAR
**Version:** 2.1 (v2.0 removiendo SERVICE_KEY en plano, clarificando ejecutor)

> **Nota de rol:** El PJM prepara y valida, no ejecuta. Este HO debe ser ejecutado por PM o DO con credenciales en entorno. El PJM valida el resultado despues y reporta.

---

## 0. OBJETIVO

Las 116 tareas YA ESTAN CREADAS en VTT como `MEM-001` a `MEM-116`. Este HO define el trabajo pendiente de ejecucion sobre esas tareas:

1. **Asignar agente** a cada tarea (PATCH `assigneeId`)
2. **Ajustar** `complexity`, `category`, `estimatedHours` si difieren del plan
3. **Validar** mapeo task → delivery (gotcha API — ver §5)
4. **Crear** dependencias criticas (MEM-081 → MEM-038, etc.) — pendiente endpoint
5. **Reportar** al PM

**NO crear tareas.** Las tareas ya existen. Si el script intenta POST va a generar duplicados.

### Responsabilidades

| Rol | Accion |
|-----|--------|
| PJM (yo) | Preparar este HO, validar plan, revisar resultado, reportar al PM |
| PM / DO | Ejecutar el script con SERVICE_KEY en entorno |
| Agentes asignados | Ver sus tareas en VTT despues de ejecucion exitosa |

---

## 1. DATOS DE CONEXION

| Dato | Valor |
|------|-------|
| **Project ID** | `51e169f7-8a23-4628-8b78-04864b633ac7` |
| Project Key | MEM |
| API URL | http://77.42.88.106:3000 |
| PJM UUID | 0ff63a29-0bc0-465a-b9bd-5f71476bc91d |
| SERVICE_KEY | **NO EN ESTE DOCUMENTO** — leer de variable de entorno `MEM_VTT_SERVICE_KEY` |

### Setup previo a ejecucion (una sola vez)

```bash
# Linux / macOS
export MEM_VTT_SERVICE_KEY="<service-key-provista-por-PM>"

# Windows PowerShell
$env:MEM_VTT_SERVICE_KEY = "<service-key-provista-por-PM>"

# Windows CMD
set MEM_VTT_SERVICE_KEY=<service-key-provista-por-PM>
```

La SERVICE_KEY real la provee el PM directamente al ejecutor. **NO debe escribirse en ningun archivo versionado.**

---

## 2. PHASE UUIDs REALES

| Order | Fase | Phase UUID | Tareas | Horas |
|-------|------|-----------|--------|-------|
| 1 | Project Setup | `83f56bad-7e60-4ffa-bc19-9c0f9ba097a1` | 5 (MEM-001..005) | 11h |
| 2 | Discovery | `3ee3a429-f836-45ea-afde-1753c78db9ac` | 4 (MEM-006..009) | 9h |
| 3 | Planning | `a0dcfb69-b862-4784-b8c9-5aad233dfb9d` | 8 (MEM-010..017) | 23h |
| 4 | Analysis | `26ecb1f6-1eb8-494f-930e-7e173c4ee559` | 8 (MEM-018..025) | 41h |
| 5 | Design UX/UI | `2c8f0f2f-992a-46e5-b80f-9739180c2532` | 13 (MEM-026..038) | 35h |
| 6 | Design Technical | `5f452a38-6cc6-4bbc-a8d5-1f50da2562af` | 9 (MEM-039..047) | 45h |
| 7 | Development | `c2804591-b21c-4340-9065-59fd23e14b63` | 46 (MEM-048..093) | 116h |
| 8 | Testing | `7ab83ed0-2238-4241-a915-8a957144d63e` | 10 (MEM-094..103) | 60h |
| 9 | Deploy | `137d3082-f280-48da-81e7-abd3c1789f63` | 7 (MEM-104..110) | 26h |
| 10 | Operations | `2ffc2179-2376-4197-93d1-56a878cd976e` | 6 (MEM-111..116) | 15h |
| **TOTAL** | | | **116** | **381h** |

---

## 3. AGENT UUIDs

| Sigla | UUID |
|-------|------|
| PM | 350831b2-e1ae-4dbe-b2eb-7e023ec2e103 |
| PJM | 0ff63a29-0bc0-465a-b9bd-5f71476bc91d |
| TL | 92225290-6b6b-4c1f-a940-dcb4262507aa |
| BE | ebbe3cee-abed-4b3b-860d-0a81f632b08a |
| DB | 6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7 |
| FE | d23c9cd9-a156-433b-8900-94add5488eec |
| QA | 613c9538-658c-45fe-a6d7-c1ea9ff04b78 |
| DO | 322e3745-9756-4a7c-af11-44b33edef44d |
| DL | b3a09269-cded-468c-a475-15a48f203cb0 |
| UX | a75a1dae-754a-4b6f-a3ff-db8d51f6a91b |
| SA | 0c128e3b-db3b-4e31-b107-0379b5791233 |
| AR | e9403c25-c1f8-4b64-b2ef-f447d53115e2 |

---

## 4. PRIORIDADES VTT

| Prioridad | UUID | Regla |
|-----------|------|-------|
| high | `1a617554-6319-4c56-826f-8ef49a0ff9cc` | complexity = HIGH |
| medium | `d0b619ef-27e7-42d8-8879-41030a602eed` | complexity = MEDIUM o LOW |

---

## 5. API — GOTCHAS CONFIRMADOS

| # | Gotcha | Implicacion |
|---|--------|-------------|
| 1 | `POST /api/projects` ignora `deliverables[]` | Deliveries creadas por endpoint dedicado (ya hecho) |
| 2 | POST y PATCH task **aceptan** `deliveryId` pero **NO lo persisten** | GET task no devuelve `deliveryId`. Link queda sin validar — documentar como issue |
| 3 | `POST /api/phases/:id/tasks` ignora `assigneeId` | Usar PATCH posterior — este script lo hace asi |
| 4 | Inconsistencia naming: POST `/deliverables` vs GET `/deliveries` | No afecta este script (ya pasado) |

**Patron confirmado:** PATCH `/api/tasks/{taskId}` con `assigneeId`, `complexity`, `category`, `estimatedHours`, `priorityId` funciona.

---

## 6. DELIVERY UUIDs (por si se habilita task-delivery link)

### Project Setup
| Delivery UUID | Name | Tasks target |
|---------------|------|--------------|
| `020d7a9e-1dec-47e9-b157-c138a2754188` | Project Foundation Ready | MEM-001..005 |

### Discovery
| Delivery UUID | Name | Tasks target |
|---------------|------|--------------|
| `7e062012-8dc3-41c8-9db6-587bd522fae5` | Problem Definition | MEM-006, MEM-007 |
| `46747b7f-5aa2-4224-b2f8-c5b7aa2fc695` | Value Proposition | MEM-008, MEM-009 |

### Planning
| Delivery UUID | Name | Tasks target |
|---------------|------|--------------|
| `1553a1bb-bbb6-4001-a1bd-e55604fddf5f` | Vision & Objectives | MEM-010, MEM-011 |
| `aad0f343-e275-4016-b05d-ddc668da4540` | Scope | MEM-012 |
| `d43385a3-2af5-4360-9360-9027f7e5fc05` | Stakeholders | MEM-013 |
| `beb200d7-ec93-440b-8e2e-315641fb817b` | Risks | MEM-014 |
| `d81d0a16-fb85-42df-9840-10cf953dbf2b` | Timeline | MEM-015, MEM-016 |
| `26231124-d702-4fbf-becf-b804e14f53ff` | Budget & Resources | MEM-017 |

### Analysis
| Delivery UUID | Name | Tasks target |
|---------------|------|--------------|
| `6ac31b6c-490b-49cc-aedf-9d0d6bd7cbbc` | Functional Requirements | MEM-018 |
| `cb635bb1-fd85-4c94-acba-1207f72cb033` | Non-Functional Requirements | MEM-019 |
| `a5ebe11c-4989-4107-9ec7-6c4b15b2cb01` | Use Cases | MEM-020 |
| `0cc1246e-8a2e-4d0e-95c6-bad1cb44c9d8` | User Stories | MEM-021 |
| `ab5cd01a-b1a7-46ac-8c7d-415af03018b4` | Business Rules | MEM-022 |
| `93ff3616-9750-4d3a-bae3-3618be821da9` | User Flows | MEM-023 |
| `65e3a6e2-9296-4dc1-9f05-0e1c13879332` | Acceptance Criteria | MEM-024 |
| `5d38464a-a2da-482f-8db7-d6a9c86560fa` | Traceability Matrix | MEM-025 |

### Design UX/UI
| Delivery UUID | Name | Tasks target |
|---------------|------|--------------|
| `64487f12-0696-4e24-b973-39da1e3e25fd` | Personas | MEM-026 |
| `335688d7-bb95-4223-a79d-ed53ad1bdc46` | Information Architecture | MEM-027 |
| `c07dbe80-389b-4b39-aaf6-0eda69063b73` | Design System | MEM-028 |
| `171bb08d-10f8-49ad-a7c7-7b592924e2b4` | Wireframes | MEM-029..036 |
| `d0429a60-066c-49e4-99ca-a234b757924c` | Mockups UI Design | MEM-031, MEM-032 (compartido con Wireframes) |
| `ae0a6c01-644b-4063-9230-7670955390c7` | Design Handoff | MEM-037, MEM-038 |

### Design Technical
| Delivery UUID | Name | Tasks target |
|---------------|------|--------------|
| `45a98395-2b39-412d-86f8-c38619e65808` | Solution Architecture | MEM-039 |
| `876c7e9a-e9c3-4859-825b-4f24c16db0d5` | Code Architecture | MEM-040 |
| `042828c8-d1e0-470c-904b-3acfb3afdafc` | Database Design | MEM-041 |
| `f30e7d4d-bd75-46d5-9b9e-35e4d2648182` | API Design | MEM-042 |
| `e05c0252-260a-48cc-bd48-e84030bd2771` | Sequence Diagrams | MEM-043 |
| `9a52a704-e7e5-4df4-93e7-0c01a9b12937` | Architecture Decision Records | MEM-044 |
| `60745748-e84d-4ca1-af44-ee936a1e678b` | Security Plan | MEM-045 |
| `bb4bd482-ba4a-4435-ad78-67bf55ad6717` | Infrastructure Plan | MEM-046 |
| `dc564fd8-8b98-435d-8048-781f1fefa3f2` | Technical Estimates | MEM-047 |

### Development
| Delivery UUID | Name | Tasks target |
|---------------|------|--------------|
| `cdf64298-78a3-41f0-81ca-c6cc620b0e6b` | S01: Schema + Seeds | MEM-048..052 |
| `6225b7f9-1c53-4d15-bf58-28356f5c2abe` | S02: Import + Timeline | MEM-053..057 |
| `07fc4bb5-0bea-4ca3-b220-ec72f07b0d7f` | S03: Content + Context | MEM-058..062 |
| `307fde68-d46e-4d27-b214-5a7578248cd3` | S04: Adapters + Cleanup | MEM-063..068 |
| `91d5b816-a2e5-40c0-922d-7680cfffc18c` | S05: Lista + Cost + Dashboard | MEM-069..074 |
| `07af8788-bf9d-4f79-9fdc-9f9b6991e5f5` | S06: Docker + Integration | MEM-075..080 |
| `a68364fb-f3c4-4a83-a781-73c07740f98c` | UI-01: Setup + Timeline + Viewer | MEM-081..085 |
| `0faec639-adc7-4b54-8473-341304d675a0` | UI-02: Dashboard + Cost + Import | MEM-086..088 |
| `40ac1259-720c-4fdc-bd0e-5e8a3034ec63` | UI-03: Viewer REVIEW + Lista | MEM-089, MEM-090 |
| `06c47e49-0d9f-496c-b929-5426bdf03176` | UI-04: Cost Agente + Health | MEM-091..093 |

### Testing
| Delivery UUID | Name | Tasks target |
|---------------|------|--------------|
| `69ab8133-76be-4651-9005-bef9a065e765` | Test Planning | MEM-094 |
| `4c1c3824-ab69-48cf-8e37-733182f2ce12` | Test Cases | MEM-095 |
| `2c8fdfc2-58cd-4e8e-a635-ef6a6e37ec6d` | Test Environment | MEM-096 |
| `05201e04-8833-4f55-acfd-3d2911c1a4e7` | Functional Testing | MEM-097 |
| `9d59355e-ffbe-43df-9c6d-cc730ddbb6d1` | Integration Testing | MEM-098 |
| `b9cdfc52-6d4f-4322-8490-5f96c6035c9d` | E2E Testing | MEM-099 |
| `cdb3747f-6f7c-4297-aef3-41bdd61de9b2` | Performance Testing | MEM-100 |
| `41f0bd77-2a8d-439f-a649-37b4f97b86dc` | Security Testing | MEM-101 |
| `8bcc3f68-8a41-40c8-b7ea-f1797dbd5a68` | UAT | MEM-102 |
| `a7ab2609-725b-428c-afed-dca2540e8c03` | Bug Fixes | MEM-103 |

### Deploy
| Delivery UUID | Name | Tasks target |
|---------------|------|--------------|
| `94655325-9812-48b3-898a-941773d043da` | Infrastructure Setup | MEM-104 |
| `718394eb-b86e-47f5-b50c-d9a9f958df1a` | CI/CD Configuration | MEM-105 |
| `84efdaa0-dbe7-4513-99e9-0708739e9bf6` | Staging Deploy | MEM-106 |
| `cf1bf126-039b-4c6d-b069-7f4e036116b3` | Smoke Testing | MEM-107 |
| `76051806-a2b9-4ec9-b9f4-961523cc4b97` | Production Deploy | MEM-108 |
| `57291868-e1e2-4b62-bee1-5f20d49ad5a6` | Post-Deploy Monitoring | MEM-109 |
| `d28a5a78-829e-4ea0-86ec-eee556e181bd` | Rollback Plan | MEM-110 |

### Operations
| Delivery UUID | Name | Tasks target |
|---------------|------|--------------|
| `02ff2c77-8ea9-424c-b0db-077b819541d0` | Monitoring | MEM-111 |
| `dfd61eca-7194-4835-b25f-51f9956c63e6` | User Support | MEM-112 |
| `813c2946-4bb8-4f77-a7c3-e24061842b4f` | Bug Fixes Operations | MEM-113 |
| `8cdde41d-147f-4e2c-b234-0952d560b614` | Incremental Improvements | MEM-114 |
| `a8a4df88-cb3b-4ff8-af95-e25c3883693e` | Security Updates | MEM-115 |
| `fdcf5a75-25b2-46f4-b260-3429a8f9f41b` | Scaling | MEM-116 |

---

## 7. SCRIPT DE EJECUCION (PATCH)

```python
#!/usr/bin/env python3
"""
ACTUALIZAR_TAREAS_VTT.py
Actualiza las 116 tareas ya creadas en VTT con assigneeId y deltas.
Origen: HANDOFF_PJM_SPRINT_SETUP_VTT.md v3.0
Ejecutor: PM o DO (con MEM_VTT_SERVICE_KEY en entorno).
"""

import os
import sys
import urllib.request
import urllib.error
import json
import time

# ============================================================
# CONFIGURACION
# ============================================================

BASE_URL   = "http://77.42.88.106:3000"
PROJECT_ID = "51e169f7-8a23-4628-8b78-04864b633ac7"
PJM_ID     = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"

# SERVICE_KEY se lee de variable de entorno — NO hardcodear
SK = os.environ.get("MEM_VTT_SERVICE_KEY")
if not SK:
    sys.exit("ERROR: variable MEM_VTT_SERVICE_KEY no definida. Ver HO seccion 1.")

AGENTS = {
    "PM":  "350831b2-e1ae-4dbe-b2eb-7e023ec2e103",
    "PJM": "0ff63a29-0bc0-465a-b9bd-5f71476bc91d",
    "TL":  "92225290-6b6b-4c1f-a940-dcb4262507aa",
    "BE":  "ebbe3cee-abed-4b3b-860d-0a81f632b08a",
    "DB":  "6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7",
    "FE":  "d23c9cd9-a156-433b-8900-94add5488eec",
    "QA":  "613c9538-658c-45fe-a6d7-c1ea9ff04b78",
    "DO":  "322e3745-9756-4a7c-af11-44b33edef44d",
    "DL":  "b3a09269-cded-468c-a475-15a48f203cb0",
    "UX":  "a75a1dae-754a-4b6f-a3ff-db8d51f6a91b",
    "SA":  "0c128e3b-db3b-4e31-b107-0379b5791233",
    "AR":  "e9403c25-c1f8-4b64-b2ef-f447d53115e2",
}

PRIORITY = {
    "HIGH":   "1a617554-6319-4c56-826f-8ef49a0ff9cc",
    "MEDIUM": "d0b619ef-27e7-42d8-8879-41030a602eed",
    "LOW":    "d0b619ef-27e7-42d8-8879-41030a602eed",
}

# Plan esperado: task_key -> (agent, hours, complexity, category, delivery_uuid)
PLAN = {
    # Project Setup
    "MEM-001": ("DO",  2, "MEDIUM", "deployment",    "020d7a9e-1dec-47e9-b157-c138a2754188"),
    "MEM-002": ("PJM", 2, "LOW",    "documentation", "020d7a9e-1dec-47e9-b157-c138a2754188"),
    "MEM-003": ("PJM", 1, "LOW",    "documentation", "020d7a9e-1dec-47e9-b157-c138a2754188"),
    "MEM-004": ("DO",  2, "MEDIUM", "deployment",    "020d7a9e-1dec-47e9-b157-c138a2754188"),
    "MEM-005": ("PM",  4, "MEDIUM", "documentation", "020d7a9e-1dec-47e9-b157-c138a2754188"),
    # Discovery
    "MEM-006": ("SA",  3, "MEDIUM", "documentation", "7e062012-8dc3-41c8-9db6-587bd522fae5"),
    "MEM-007": ("PM",  2, "LOW",    "review",        "7e062012-8dc3-41c8-9db6-587bd522fae5"),
    "MEM-008": ("SA",  3, "MEDIUM", "documentation", "46747b7f-5aa2-4224-b2f8-c5b7aa2fc695"),
    "MEM-009": ("PM",  1, "LOW",    "review",        "46747b7f-5aa2-4224-b2f8-c5b7aa2fc695"),
    # Planning
    "MEM-010": ("PM",  3, "MEDIUM", "documentation", "1553a1bb-bbb6-4001-a1bd-e55604fddf5f"),
    "MEM-011": ("PM",  2, "MEDIUM", "documentation", "1553a1bb-bbb6-4001-a1bd-e55604fddf5f"),
    "MEM-012": ("SA",  4, "HIGH",   "documentation", "aad0f343-e275-4016-b05d-ddc668da4540"),
    "MEM-013": ("PJM", 2, "LOW",    "documentation", "d43385a3-2af5-4360-9360-9027f7e5fc05"),
    "MEM-014": ("PJM", 3, "MEDIUM", "documentation", "beb200d7-ec93-440b-8e2e-315641fb817b"),
    "MEM-015": ("PJM", 4, "HIGH",   "documentation", "d81d0a16-fb85-42df-9840-10cf953dbf2b"),
    "MEM-016": ("PJM", 3, "MEDIUM", "documentation", "d81d0a16-fb85-42df-9840-10cf953dbf2b"),
    "MEM-017": ("PM",  2, "LOW",    "documentation", "26231124-d702-4fbf-becf-b804e14f53ff"),
    # Analysis
    "MEM-018": ("SA",  6, "HIGH",   "documentation", "6ac31b6c-490b-49cc-aedf-9d0d6bd7cbbc"),
    "MEM-019": ("AR",  4, "HIGH",   "documentation", "cb635bb1-fd85-4c94-acba-1207f72cb033"),
    "MEM-020": ("SA",  5, "MEDIUM", "documentation", "a5ebe11c-4989-4107-9ec7-6c4b15b2cb01"),
    "MEM-021": ("SA",  8, "HIGH",   "documentation", "0cc1246e-8a2e-4d0e-95c6-bad1cb44c9d8"),
    "MEM-022": ("TL",  4, "HIGH",   "documentation", "ab5cd01a-b1a7-46ac-8c7d-415af03018b4"),
    "MEM-023": ("UX",  4, "MEDIUM", "design",        "93ff3616-9750-4d3a-bae3-3618be821da9"),
    "MEM-024": ("SA",  6, "HIGH",   "documentation", "65e3a6e2-9296-4dc1-9f05-0e1c13879332"),
    "MEM-025": ("SA",  4, "MEDIUM", "documentation", "5d38464a-a2da-482f-8db7-d6a9c86560fa"),
    # Design UX/UI
    "MEM-026": ("UX",  3, "MEDIUM", "design",        "64487f12-0696-4e24-b973-39da1e3e25fd"),
    "MEM-027": ("UX",  4, "MEDIUM", "design",        "335688d7-bb95-4223-a79d-ed53ad1bdc46"),
    "MEM-028": ("DL",  3, "MEDIUM", "design",        "c07dbe80-389b-4b39-aaf6-0eda69063b73"),
    "MEM-029": ("DL",  4, "HIGH",   "design",        "171bb08d-10f8-49ad-a7c7-7b592924e2b4"),
    "MEM-030": ("DL",  3, "MEDIUM", "design",        "171bb08d-10f8-49ad-a7c7-7b592924e2b4"),
    "MEM-031": ("DL",  4, "HIGH",   "design",        "171bb08d-10f8-49ad-a7c7-7b592924e2b4"),
    "MEM-032": ("DL",  4, "HIGH",   "design",        "171bb08d-10f8-49ad-a7c7-7b592924e2b4"),
    "MEM-033": ("DL",  2, "MEDIUM", "design",        "171bb08d-10f8-49ad-a7c7-7b592924e2b4"),
    "MEM-034": ("DL",  2, "MEDIUM", "design",        "171bb08d-10f8-49ad-a7c7-7b592924e2b4"),
    "MEM-035": ("DL",  2, "MEDIUM", "design",        "171bb08d-10f8-49ad-a7c7-7b592924e2b4"),
    "MEM-036": ("DL",  1, "LOW",    "design",        "171bb08d-10f8-49ad-a7c7-7b592924e2b4"),
    "MEM-037": ("DL",  2, "MEDIUM", "documentation", "ae0a6c01-644b-4063-9230-7670955390c7"),
    "MEM-038": ("DL",  1, "LOW",    "documentation", "ae0a6c01-644b-4063-9230-7670955390c7"),
    # Design Technical
    "MEM-039": ("TL",  6, "HIGH",   "documentation", "45a98395-2b39-412d-86f8-c38619e65808"),
    "MEM-040": ("TL",  4, "HIGH",   "documentation", "876c7e9a-e9c3-4859-825b-4f24c16db0d5"),
    "MEM-041": ("DB",  6, "HIGH",   "documentation", "042828c8-d1e0-470c-904b-3acfb3afdafc"),
    "MEM-042": ("BE",  8, "HIGH",   "documentation", "f30e7d4d-bd75-46d5-9b9e-35e4d2648182"),
    "MEM-043": ("AR",  6, "HIGH",   "documentation", "e05c0252-260a-48cc-bd48-e84030bd2771"),
    "MEM-044": ("TL",  4, "MEDIUM", "documentation", "9a52a704-e7e5-4df4-93e7-0c01a9b12937"),
    "MEM-045": ("AR",  4, "HIGH",   "documentation", "60745748-e84d-4ca1-af44-ee936a1e678b"),
    "MEM-046": ("DO",  4, "MEDIUM", "documentation", "bb4bd482-ba4a-4435-ad78-67bf55ad6717"),
    "MEM-047": ("TL",  3, "MEDIUM", "documentation", "dc564fd8-8b98-435d-8048-781f1fefa3f2"),
    # Development — S01
    "MEM-048": ("DB",  3, "HIGH",   "development",   "cdf64298-78a3-41f0-81ca-c6cc620b0e6b"),
    "MEM-049": ("DB",  2, "MEDIUM", "development",   "cdf64298-78a3-41f0-81ca-c6cc620b0e6b"),
    "MEM-050": ("DB",  1, "LOW",    "development",   "cdf64298-78a3-41f0-81ca-c6cc620b0e6b"),
    "MEM-051": ("BE",  2, "MEDIUM", "development",   "cdf64298-78a3-41f0-81ca-c6cc620b0e6b"),
    "MEM-052": ("BE",  1, "LOW",    "development",   "cdf64298-78a3-41f0-81ca-c6cc620b0e6b"),
    # Development — S02
    "MEM-053": ("BE",  4, "HIGH",   "development",   "6225b7f9-1c53-4d15-bf58-28356f5c2abe"),
    "MEM-054": ("BE",  2, "MEDIUM", "development",   "6225b7f9-1c53-4d15-bf58-28356f5c2abe"),
    "MEM-055": ("BE",  3, "HIGH",   "development",   "6225b7f9-1c53-4d15-bf58-28356f5c2abe"),
    "MEM-056": ("BE",  2, "MEDIUM", "development",   "6225b7f9-1c53-4d15-bf58-28356f5c2abe"),
    "MEM-057": ("BE",  1, "LOW",    "development",   "6225b7f9-1c53-4d15-bf58-28356f5c2abe"),
    # Development — S03
    "MEM-058": ("BE",  2, "MEDIUM", "development",   "07fc4bb5-0bea-4ca3-b220-ec72f07b0d7f"),
    "MEM-059": ("BE",  4, "HIGH",   "development",   "07fc4bb5-0bea-4ca3-b220-ec72f07b0d7f"),
    "MEM-060": ("BE",  2, "HIGH",   "development",   "07fc4bb5-0bea-4ca3-b220-ec72f07b0d7f"),
    "MEM-061": ("QA",  2, "MEDIUM", "testing",       "07fc4bb5-0bea-4ca3-b220-ec72f07b0d7f"),
    "MEM-062": ("QA",  2, "MEDIUM", "testing",       "07fc4bb5-0bea-4ca3-b220-ec72f07b0d7f"),
    # Development — S04
    "MEM-063": ("BE",  3, "MEDIUM", "development",   "307fde68-d46e-4d27-b214-5a7578248cd3"),
    "MEM-064": ("BE",  2, "MEDIUM", "development",   "307fde68-d46e-4d27-b214-5a7578248cd3"),
    "MEM-065": ("BE",  2, "MEDIUM", "development",   "307fde68-d46e-4d27-b214-5a7578248cd3"),
    "MEM-066": ("BE",  2, "MEDIUM", "development",   "307fde68-d46e-4d27-b214-5a7578248cd3"),
    "MEM-067": ("BE",  1, "LOW",    "development",   "307fde68-d46e-4d27-b214-5a7578248cd3"),
    "MEM-068": ("BE",  2, "MEDIUM", "testing",       "307fde68-d46e-4d27-b214-5a7578248cd3"),
    # Development — S05
    "MEM-069": ("BE",  2, "MEDIUM", "development",   "91d5b816-a2e5-40c0-922d-7680cfffc18c"),
    "MEM-070": ("BE",  2, "MEDIUM", "development",   "91d5b816-a2e5-40c0-922d-7680cfffc18c"),
    "MEM-071": ("BE",  2, "MEDIUM", "development",   "91d5b816-a2e5-40c0-922d-7680cfffc18c"),
    "MEM-072": ("BE",  2, "MEDIUM", "development",   "91d5b816-a2e5-40c0-922d-7680cfffc18c"),
    "MEM-073": ("BE",  2, "MEDIUM", "development",   "91d5b816-a2e5-40c0-922d-7680cfffc18c"),
    "MEM-074": ("BE",  1, "LOW",    "development",   "91d5b816-a2e5-40c0-922d-7680cfffc18c"),
    # Development — S06
    "MEM-075": ("DO",  2, "MEDIUM", "deployment",    "07af8788-bf9d-4f79-9fdc-9f9b6991e5f5"),
    "MEM-076": ("DO",  2, "MEDIUM", "deployment",    "07af8788-bf9d-4f79-9fdc-9f9b6991e5f5"),
    "MEM-077": ("DO",  1, "LOW",    "deployment",    "07af8788-bf9d-4f79-9fdc-9f9b6991e5f5"),
    "MEM-078": ("BE",  4, "HIGH",   "development",   "07af8788-bf9d-4f79-9fdc-9f9b6991e5f5"),
    "MEM-079": ("QA",  3, "HIGH",   "testing",       "07af8788-bf9d-4f79-9fdc-9f9b6991e5f5"),
    "MEM-080": ("QA",  2, "MEDIUM", "testing",       "07af8788-bf9d-4f79-9fdc-9f9b6991e5f5"),
    # Development — UI-01
    "MEM-081": ("FE",  2, "MEDIUM", "development",   "a68364fb-f3c4-4a83-a781-73c07740f98c"),
    "MEM-082": ("FE",  1, "LOW",    "development",   "a68364fb-f3c4-4a83-a781-73c07740f98c"),
    "MEM-083": ("FE",  5, "HIGH",   "development",   "a68364fb-f3c4-4a83-a781-73c07740f98c"),
    "MEM-084": ("FE",  6, "HIGH",   "development",   "a68364fb-f3c4-4a83-a781-73c07740f98c"),
    "MEM-085": ("FE",  2, "MEDIUM", "development",   "a68364fb-f3c4-4a83-a781-73c07740f98c"),
    # Development — UI-02
    "MEM-086": ("FE",  4, "HIGH",   "development",   "0faec639-adc7-4b54-8473-341304d675a0"),
    "MEM-087": ("FE",  4, "MEDIUM", "development",   "0faec639-adc7-4b54-8473-341304d675a0"),
    "MEM-088": ("FE",  4, "MEDIUM", "development",   "0faec639-adc7-4b54-8473-341304d675a0"),
    # Development — UI-03
    "MEM-089": ("FE",  5, "HIGH",   "development",   "40ac1259-720c-4fdc-bd0e-5e8a3034ec63"),
    "MEM-090": ("FE",  5, "HIGH",   "development",   "40ac1259-720c-4fdc-bd0e-5e8a3034ec63"),
    # Development — UI-04
    "MEM-091": ("FE",  3, "MEDIUM", "development",   "06c47e49-0d9f-496c-b929-5426bdf03176"),
    "MEM-092": ("FE",  2, "LOW",    "development",   "06c47e49-0d9f-496c-b929-5426bdf03176"),
    "MEM-093": ("FE",  3, "MEDIUM", "development",   "06c47e49-0d9f-496c-b929-5426bdf03176"),
    # Testing
    "MEM-094": ("QA",  4, "MEDIUM", "documentation", "69ab8133-76be-4651-9005-bef9a065e765"),
    "MEM-095": ("QA",  8, "HIGH",   "testing",       "4c1c3824-ab69-48cf-8e37-733182f2ce12"),
    "MEM-096": ("DO",  4, "MEDIUM", "deployment",    "2c8fdfc2-58cd-4e8e-a635-ef6a6e37ec6d"),
    "MEM-097": ("QA",  8, "HIGH",   "testing",       "05201e04-8833-4f55-acfd-3d2911c1a4e7"),
    "MEM-098": ("QA",  6, "HIGH",   "testing",       "9d59355e-ffbe-43df-9c6d-cc730ddbb6d1"),
    "MEM-099": ("QA",  8, "HIGH",   "testing",       "b9cdfc52-6d4f-4322-8490-5f96c6035c9d"),
    "MEM-100": ("QA",  6, "HIGH",   "testing",       "cdb3747f-6f7c-4297-aef3-41bdd61de9b2"),
    "MEM-101": ("AR",  4, "HIGH",   "testing",       "41f0bd77-2a8d-439f-a649-37b4f97b86dc"),
    "MEM-102": ("PM",  4, "MEDIUM", "review",        "8bcc3f68-8a41-40c8-b7ea-f1797dbd5a68"),
    "MEM-103": ("BE",  8, "HIGH",   "bugfix",        "a7ab2609-725b-428c-afed-dca2540e8c03"),
    # Deploy
    "MEM-104": ("DO",  4, "MEDIUM", "deployment",    "94655325-9812-48b3-898a-941773d043da"),
    "MEM-105": ("DO",  6, "HIGH",   "deployment",    "718394eb-b86e-47f5-b50c-d9a9f958df1a"),
    "MEM-106": ("DO",  4, "MEDIUM", "deployment",    "84efdaa0-dbe7-4513-99e9-0708739e9bf6"),
    "MEM-107": ("QA",  3, "MEDIUM", "testing",       "cf1bf126-039b-4c6d-b069-7f4e036116b3"),
    "MEM-108": ("DO",  4, "HIGH",   "deployment",    "76051806-a2b9-4ec9-b9f4-961523cc4b97"),
    "MEM-109": ("DO",  3, "MEDIUM", "review",        "57291868-e1e2-4b62-bee1-5f20d49ad5a6"),
    "MEM-110": ("TL",  2, "MEDIUM", "documentation", "d28a5a78-829e-4ea0-86ec-eee556e181bd"),
    # Operations
    "MEM-111": ("DO",  3, "MEDIUM", "review",        "02ff2c77-8ea9-424c-b0db-077b819541d0"),
    "MEM-112": ("PM",  2, "LOW",    "documentation", "dfd61eca-7194-4835-b25f-51f9956c63e6"),
    "MEM-113": ("TL",  2, "MEDIUM", "documentation", "813c2946-4bb8-4f77-a7c3-e24061842b4f"),
    "MEM-114": ("PM",  3, "MEDIUM", "documentation", "8cdde41d-147f-4e2c-b234-0952d560b614"),
    "MEM-115": ("AR",  2, "MEDIUM", "documentation", "a8a4df88-cb3b-4ff8-af95-e25c3883693e"),
    "MEM-116": ("AR",  3, "HIGH",   "documentation", "fdcf5a75-25b2-46f4-b260-3429a8f9f41b"),
}

# ============================================================
# HELPERS
# ============================================================

def get_token():
    req = urllib.request.Request(
        BASE_URL + "/api/auth/service-token",
        data=json.dumps({"userId": PJM_ID, "serviceKey": SK}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["data"]["token"]


def get_all_project_tasks(token):
    """Retorna mapping: task_key (e.g. MEM-001) -> task UUID."""
    req = urllib.request.Request(
        BASE_URL + f"/api/tasks?projectId={PROJECT_ID}",
        headers={"Authorization": "Bearer " + token},
    )
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    tasks = data.get("data", data) if isinstance(data, dict) else data
    mapping = {}
    for t in tasks:
        key = t.get("key") or t.get("taskKey") or t.get("code")
        tid = t.get("id")
        if key and tid:
            mapping[key] = tid
    return mapping


def patch_task(token, task_id, body):
    req = urllib.request.Request(
        BASE_URL + f"/api/tasks/{task_id}",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type":  "application/json",
        },
        method="PATCH",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:200]}"
    except Exception as e:
        return None, str(e)


# ============================================================
# EJECUCION
# ============================================================

def main():
    print("=== VTT Task Updater: Memory Service ===")
    print(f"Project: {PROJECT_ID}")
    print("Obteniendo token...")
    token = get_token()
    print("Token OK.\n")

    print("Obteniendo mapping MEM-XXX -> task UUID...")
    mapping = get_all_project_tasks(token)
    print(f"Tareas encontradas: {len(mapping)}\n")

    missing = [k for k in PLAN.keys() if k not in mapping]
    if missing:
        print(f"ALERTA: {len(missing)} tareas no encontradas en VTT:")
        for k in missing[:10]:
            print(f"  - {k}")
        if len(missing) > 10:
            print(f"  ... y {len(missing)-10} mas")
        print("Abortando. Verificar que las tareas existan antes de re-ejecutar.")
        sys.exit(1)

    ok, fail, no_delivery = 0, 0, 0
    for task_key, (agent, hours, complexity, category, delivery_uuid) in PLAN.items():
        task_id = mapping[task_key]
        body = {
            "assigneeId":     AGENTS[agent],
            "estimatedHours": hours,
            "complexity":     complexity,
            "category":       category,
            "priorityId":     PRIORITY[complexity],
            "deliveryId":     delivery_uuid,  # puede ser ignorado — gotcha §5
        }
        _, err = patch_task(token, task_id, body)
        if err:
            fail += 1
            print(f"  [FAIL] {task_key} -> {err}")
        else:
            ok += 1
            print(f"  [OK]   {task_key} {agent:<4} {hours:>2}h {complexity:<6} {category}")
        time.sleep(0.15)

    print("\n=== RESUMEN ===")
    print(f"OK:   {ok}")
    print(f"FAIL: {fail}")

    # Validar persistencia de deliveryId en una muestra (gotcha §5)
    print("\nValidando persistencia de deliveryId (muestra de 3 tareas)...")
    sample_keys = ["MEM-001", "MEM-048", "MEM-081"]
    for sk in sample_keys:
        if sk not in mapping:
            continue
        req = urllib.request.Request(
            BASE_URL + f"/api/tasks/{mapping[sk]}",
            headers={"Authorization": "Bearer " + token},
        )
        with urllib.request.urlopen(req) as r:
            t = json.loads(r.read())
            t = t.get("data", t)
        did = t.get("deliveryId") or t.get("deliverableId")
        aid = t.get("assigneeId")
        print(f"  {sk}: assigneeId={'OK' if aid else 'MISSING'}, deliveryId={'OK' if did else 'NOT PERSISTED'}")

    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
```

---

## 8. PLAN DE EJECUCION

**Quien ejecuta:** PM o DO con permisos operativos.
**Quien valida despues:** PJM.

Pasos:

1. PM provee la SERVICE_KEY al ejecutor (fuera de banda, no por este archivo).
2. Ejecutor exporta la variable de entorno (ver §1).
3. Copiar el bloque de codigo a `ACTUALIZAR_TAREAS_VTT.py` (fuera del repo o en carpeta ignorada por git).
4. Ejecutar: `python3 ACTUALIZAR_TAREAS_VTT.py`
5. El script:
   - Lee `MEM_VTT_SERVICE_KEY` del entorno (falla si no existe)
   - Obtiene token JWT
   - Lista las 116 tareas del proyecto
   - Mapea `MEM-XXX` a UUID real
   - Hace PATCH a cada tarea con: `assigneeId`, `estimatedHours`, `complexity`, `category`, `priorityId`, `deliveryId`
   - Valida en una muestra si `deliveryId` persiste (gotcha §5)
6. Si hay FAIL: revisar mensaje, corregir, re-ejecutar (PATCH es idempotente)
7. Ejecutor entrega log de salida + conteo OK/FAIL al PJM para validacion.

---

## 9. CHECKLIST POST-EJECUCION

- [ ] Script corrido sin errores de auth/red
- [ ] Log muestra 116 `[OK]`, 0 `[FAIL]`
- [ ] `GET /api/projects/51e169f7-8a23-4628-8b78-04864b633ac7` → `tasksCount = 116`
- [ ] Muestra de 3 tareas: `assigneeId` persistido
- [ ] Muestra de 3 tareas: `deliveryId` status (PERSISTED o NOT PERSISTED)
- [ ] Si `deliveryId` NO persiste: **crear issue para el PM** documentando el gotcha §5
- [ ] Dependencias creadas (paso siguiente, no cubierto en este script)
- [ ] Reporte al PM

---

## 10. DEPENDENCIAS A CREAR (paso manual / siguiente script)

Este HO NO cubre la creacion de dependencias (requiere endpoint separado que aun no esta confirmado). Las dependencias minimas que se deben crear:

| From | To | Razon |
|------|-----|-------|
| MEM-048..052 | MEM-053 | S02 depende de S01 |
| MEM-053..057 | MEM-058 | S03 depende de S02 |
| MEM-058..062 | MEM-063 | S04 depende de S03 |
| MEM-063..068 | MEM-069 | S05 depende de S04 |
| MEM-069..074 | MEM-075 | S06 depende de S05 |
| MEM-038 | MEM-081 | **HITO** FE depende de Design Handoff |
| MEM-081..085 | MEM-086 | UI-02 depende de UI-01 |
| MEM-086..088 | MEM-089 | UI-03 depende de UI-02 |
| MEM-089..090 | MEM-091 | UI-04 depende de UI-03 |

Preguntar al PM cual es el endpoint VTT para crear dependencias antes de programar el script.

---

## 11. REPORTE AL PM (PLANTILLA)

```markdown
## Entrega PJM: Actualizacion de 116 tareas Memory Service

**Fecha:** [YYYY-MM-DD HH:MM]
**Proyecto:** Memory Service (51e169f7-8a23-4628-8b78-04864b633ac7)
**Origen del plan:** HANDOFF_PJM_SPRINT_SETUP_VTT.md v3.0

### Resultado PATCH
- Tareas actualizadas: [N] / 116
- Fallos: [N]

### Asignaciones por rol
| Rol | Tareas asignadas | Horas |
|-----|------------------|-------|
| PM | [N] | ~24h |
| PJM | [N] | ~15h |
| SA | [N] | ~36h |
| TL | [N] | ~25h |
| AR | [N] | ~23h |
| DB | [N] | ~12h |
| BE | [N] | ~74h |
| DL | [N] | ~28h |
| UX | [N] | ~11h |
| FE | [N] | ~46h |
| QA | [N] | ~54h |
| DO | [N] | ~33h |
| TOTAL | 116 | 381h |

### Issues encontrados
- [ ] `deliveryId` [PERSISTE / NO PERSISTE] en GET task (gotcha §5 del HO v3.0)
- [ ] Endpoint para crear dependencias: [CONFIRMADO / PENDIENTE]

### Siguiente paso
- Si deliveryId persiste: listo para kickoff Pre-Sprint
- Si no: necesito decision del PM (aceptar tareas a nivel fase vs esperar fix API)
- Dependencias: pendiente endpoint confirmado
```

---

## 12. HISTORIAL

| Version | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-04-19 | PJM | Version inicial basada en HANDOFF v2.0 (POST tareas) |
| 2.0 | 2026-04-21 | PJM | Reescrito con HANDOFF v3.0: nuevo Project ID, tareas ya creadas, PATCH en vez de POST, delivery UUIDs reales, gotchas confirmados |
| 2.1 | 2026-04-21 | PJM | **Seguridad:** SERVICE_KEY movida a variable de entorno. **Framing:** ejecutor explicito (PM/DO), PJM coordina y valida. Filename pendiente de rename. |

---

**Estado:** LISTO PARA EJECUTAR (por PM o DO)
**Siguiente:**
1. PM provee SERVICE_KEY al ejecutor (fuera de banda)
2. Ejecutor corre el script y entrega log al PJM
3. PJM valida resultado, documenta gotchas, reporta al PM
