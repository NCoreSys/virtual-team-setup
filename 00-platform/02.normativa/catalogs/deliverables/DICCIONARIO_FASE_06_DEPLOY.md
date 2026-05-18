# DICCIONARIO DE DELIVERABLES — FASE 6: DEPLOY

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 6 — Deploy  
**Total deliverables:** 38  
**Total subfases:** 7  
**Responsable de fase:** DevOps Lead  
**Aprueba:** Solution Architect

---

## Contexto de la fase

Deploy es el proceso de llevar el producto desde "código testeado" a "producto live en producción": provisionar infraestructura, configurar CI/CD pipelines, desplegar a staging, ejecutar smoke tests, desplegar a producción, configurar monitoring, y preparar rollback. Es la fase más corta pero más crítica — un error aquí impacta a usuarios reales.

---

## 6.1 Infrastructure Setup (8 deliverables)

**Responsable:** DevOps Lead | **Aprueba:** Solution Architect

---

### 6.1.1 Infrastructure Ready

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.1 Infrastructure Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Servers/Cloud |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere provisionar toda la infraestructura cloud según el Infrastructure Plan (3B.8) con IaC (Terraform/Pulumi).  
En VTT: un agente puede generar archivos Terraform/Pulumi. Es bastante delegable. NO puede ejecutar provisioning sin credenciales cloud.

**Qué es:** Infraestructura de producción completamente provisionada y verificada: VPC, subnets, security groups, servidores/containers, load balancers, base de datos managed, cache, CDN, DNS, y storage. Todo implementado con IaC para que sea reproducible y versionado.

**Para qué sirve:** Sin infraestructura, no hay dónde correr el código. La infra provisionada con IaC es reproducible (destruir y recrear en minutos), versionada (cambios trackeables), y auditable.

**Inputs requeridos:**
- `3B.8.1` Infrastructure Plan — diseño a implementar
- `3B.8.2` Infrastructure Diagram — referencia visual
- `3B.8.3` Server Specifications — sizing
- `3B.8.4` Network Design — VPC/subnets/SGs
- Cloud credentials y billing approval

**Dependencias (predecessors):**
- `3B.8.1` Infrastructure Plan *(obligatorio)*
- `5.8.7` Security Sign-off *(obligatorio)*

**Habilita (successors):**
- `6.1.2` a `6.1.8` — componentes específicos
- `6.2.1` CI Pipeline — infra donde deployar
- `6.5.1` Production Deploy — infra lista

**Audiencia:**
- **DevOps Lead** — provisioning y mantenimiento
- **Solution Architect** — validación de diseño
- **Security Engineer** — security review
- **Finance** — verificación de costos

**Secciones esperadas:**
1. IaC files (Terraform/Pulumi) versionados en repo
2. Checklist de componentes provisionados
3. Verificación de cada componente (connectivity, access)
4. Cost verification vs estimate (3B.8.9)
5. Resource IDs y endpoints documentados

**Criterio de completitud:**
- [ ] Todos los componentes del Infrastructure Diagram provisionados
- [ ] IaC commiteado y reproducible
- [ ] Network connectivity verificada entre componentes
- [ ] Security groups correctos (no open to 0.0.0.0/0)
- [ ] Costos dentro del budget aprobado
- [ ] Resource IDs documentados

**Anti-patrones:**
- ❌ **Click-ops:** Crear recursos manualmente en consola — no reproducible.
- ❌ **Infra sin security review:** SGs abiertos, BD pública.
- ❌ **Sin verificación de costos:** Provisionar y descubrir 3x el budget.

**Template:** `phases/06-deploy/deliverables/infrastructure-ready.md` *(pendiente)*

---

### 6.1.2 Servers Provisioned

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.1 Infrastructure Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Config |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere provisionar compute resources (EC2, ECS, Cloud Run) con sizing correcto.  
En VTT: un agente puede generar IaC para servidores. Es altamente delegable.

**Qué es:** App servers provisionados según Server Specifications (3B.8.3): instance type, auto-scaling group con health checks, y OS/runtime. Para containerized apps: cluster (ECS/EKS) con task definitions y service settings.

**Para qué sirve:** Los servidores son donde corre el código. El sizing correcto asegura que el sistema maneja la carga esperada sin desperdicio ni performance issues.

**Inputs requeridos:**
- `3B.8.3` Server Specifications — instance types y sizing
- `3B.8.6` Scaling Strategy — auto-scaling config

**Dependencias (predecessors):**
- `6.1.1` Infrastructure Ready *(obligatorio)*
- `3B.8.3` Server Specifications *(obligatorio)*

**Habilita (successors):**
- `6.2.2` CD Pipeline — target de deployment
- `6.5.1` Production Deploy — servers donde deployar

**Audiencia:**
- **DevOps Lead** — provisioning
- **SRE** — monitoring de servers

**Secciones esperadas:**
1. Servers/containers provisionados (tabla: nombre, type, CPU, RAM, AZ)
2. Auto-scaling group config (min, max, desired, scaling policy)
3. Health check endpoints
4. OS/runtime versions
5. SSH/access configuration (bastion, IAM roles)

**Criterio de completitud:**
- [ ] Servers con instance type correcto
- [ ] Auto-scaling configurado
- [ ] Health checks funcionales
- [ ] SSH solo via bastion
- [ ] Monitoring agent instalado

**Anti-patrones:**
- ❌ **Single instance sin ASG:** Single point of failure.
- ❌ **Root SSH con password:** Usar key-based auth con bastion.
- ❌ **Sin health checks:** ASG no reemplaza instances enfermas.

**Template:** `phases/06-deploy/deliverables/servers-provisioned.md` *(pendiente)*

---

### 6.1.3 Network Configured

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.1 Infrastructure Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Config |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere configurar VPC, subnets, route tables, NAT gateway según Network Design (3B.8.4).  
En VTT: un agente puede generar IaC de networking. Es altamente delegable.

**Qué es:** Red de producción configurada: VPC con CIDR, subnets públicas (ALB, bastion) y privadas (app servers, DB, cache) en múltiples AZs, route tables, NAT gateway para egress desde subnets privadas, y VPN/peering si aplica.

**Para qué sirve:** El network design es la primera línea de defensa de seguridad. BD en subnet privada = inaccesible desde internet. Separación public/private asegura que solo lo necesario es público.

**Inputs requeridos:**
- `3B.8.4` Network Design — diseño a implementar

**Dependencias (predecessors):**
- `6.1.1` Infrastructure Ready *(obligatorio)*
- `3B.8.4` Network Design *(obligatorio)*

**Habilita (successors):**
- `6.1.4` Security Groups — SGs en la VPC
- `6.1.5` Load Balancer — LB en subnet pública
- `6.1.6` Database Ready — DB en subnet privada

**Audiencia:**
- **DevOps Lead** — configuración
- **Security Engineer** — validación de aislamiento

**Secciones esperadas:**
1. VPC (CIDR, region)
2. Subnets (tabla: nombre, CIDR, AZ, tipo public/private)
3. Route tables
4. NAT gateway para subnets privadas
5. Connectivity verificada entre componentes

**Criterio de completitud:**
- [ ] VPC creada con CIDR correcto
- [ ] Subnets public y private en al menos 2 AZs
- [ ] NAT gateway funcional
- [ ] Route tables correctas
- [ ] Connectivity verificada

**Anti-patrones:**
- ❌ **Todo en subnet pública:** BD accesible desde internet.
- ❌ **Single AZ:** Si cae la AZ, cae todo.
- ❌ **Sin NAT gateway:** Servers privados no pueden llegar a APIs externas.

**Template:** `phases/06-deploy/deliverables/network-configured.md` *(pendiente)*

---

### 6.1.4 Security Groups

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.1 Infrastructure Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Security Engineer |
| **Formato** | Config |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez + ajustes |

**Perfil de ejecución:** Requiere configurar firewall rules por componente con principle of least privilege.  
En VTT: un agente puede generar SG rules en Terraform. Es altamente delegable.

**Qué es:** Security groups configurados por componente: ALB (inbound 80/443 from 0.0.0.0/0), app servers (inbound 8080 from ALB SG only), database (inbound 5432 from app SG only), cache (inbound 6379 from app SG only), bastion (inbound 22 from office IP only). Principle of least privilege.

**Para qué sirve:** Los SGs limitan qué puede hablar con qué. Sin SGs restrictivos, cualquier componente comprometido puede acceder a cualquier otro. Con SGs, el blast radius se contiene.

**Inputs requeridos:**
- `3B.8.4` Network Design — SG rules diseñadas
- `6.1.3` Network Configured — VPC donde aplicar SGs

**Dependencias (predecessors):**
- `6.1.3` Network Configured *(obligatorio)*

**Habilita (successors):**
- Todos los componentes de infra — SGs aplican a cada recurso

**Audiencia:**
- **Security Engineer** — validación y approval
- **DevOps Lead** — configuración

**Secciones esperadas:**
1. SG por componente (tabla: SG name, component, inbound rules, outbound rules)
2. Principle of least privilege aplicado
3. Inter-SG references (no IP-based)

**Criterio de completitud:**
- [ ] SG por componente (ALB, app, DB, cache, bastion)
- [ ] Solo puertos necesarios abiertos
- [ ] Sin 0.0.0.0/0 excepto ALB 80/443
- [ ] Inter-SG references
- [ ] Validado por Security Engineer

**Anti-patrones:**
- ❌ **All ports open:** Inbound 0-65535 from 0.0.0.0/0 — sin firewall efectivo.
- ❌ **Hardcoded IPs en SGs:** Se rompe si el IP cambia.
- ❌ **DB accesible desde internet:** Critical vulnerability.

**Template:** `phases/06-deploy/deliverables/security-groups.md` *(pendiente)*

---

### 6.1.5 Load Balancer

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.1 Infrastructure Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Config |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere configurar ALB/NLB con target groups, health checks, SSL termination.  
En VTT: un agente puede generar IaC para load balancer. Es altamente delegable.

**Qué es:** ALB o NLB configurado: target groups apuntando a app servers, health check path (/health), SSL termination (HTTPS → HTTP interno), routing rules, y access logs habilitados.

**Para qué sirve:** El LB distribuye tráfico para: alta disponibilidad (si un server cae, redirige), escalabilidad (más servers = más capacidad), y SSL termination centralizado.

**Inputs requeridos:**
- `6.1.2` Servers Provisioned — targets del LB
- `6.1.8` SSL Certificates — certificado HTTPS
- `6.1.3` Network Configured — subnet pública

**Dependencias (predecessors):**
- `6.1.2` Servers Provisioned *(obligatorio)*
- `6.1.8` SSL Certificates *(obligatorio)*

**Habilita (successors):**
- `6.5.3` DNS Configured — DNS apunta al LB
- Tráfico de usuarios llega a la app

**Audiencia:**
- **DevOps Lead** — configuración
- **SRE** — monitoring del LB

**Secciones esperadas:**
1. LB type y configuración
2. Target groups (instances, ports)
3. Health check (path, interval, threshold)
4. SSL listener (port 443, certificate)
5. HTTP → HTTPS redirect
6. Access logs habilitados

**Criterio de completitud:**
- [ ] LB provisionado en subnet pública
- [ ] Target group con servers healthy
- [ ] Health check funcional (200 OK en /health)
- [ ] SSL termination con certificado válido
- [ ] HTTP → HTTPS redirect
- [ ] Access logs habilitados

**Anti-patrones:**
- ❌ **Sin health check:** LB envía tráfico a servers muertos.
- ❌ **Sin SSL:** Tráfico en HTTP plano.
- ❌ **Sin access logs:** No se puede investigar tráfico post-mortem.

**Template:** `phases/06-deploy/deliverables/load-balancer.md` *(pendiente)*

---

### 6.1.6 Database Ready

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.1 Infrastructure Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead / Database Engineer |
| **Aprueba** | Tech Lead |
| **Formato** | PostgreSQL |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere provisionar managed database con configuración de producción.  
En VTT: un agente puede generar IaC para managed DB. Es altamente delegable.

**Qué es:** BD de producción provisionada: RDS PostgreSQL con instance type según specs, storage con encryption at rest, automated backups, multi-AZ para alta disponibilidad, parameter group optimizado, y connection pooling si necesario.

**Para qué sirve:** La BD es el componente más crítico — si se pierde, se pierden los datos. Config de producción incluye: encryption (compliance), backups (recovery), multi-AZ (availability), y parameter tuning (performance).

**Inputs requeridos:**
- `3B.8.3` Server Specifications — DB instance type
- `3B.3.8` Backup Strategy — backup config
- `3B.7.5` Encryption Strategy — encryption at rest

**Dependencias (predecessors):**
- `6.1.3` Network Configured *(obligatorio)* — subnet privada
- `6.1.4` Security Groups *(obligatorio)* — SG de DB

**Habilita (successors):**
- `6.3.3` Migration Run — migrations en prod DB
- Aplicación conecta a BD

**Audiencia:**
- **Database Engineer** — configuración
- **DevOps Lead** — provisioning
- **SRE** — monitoring

**Secciones esperadas:**
1. Instance type y storage
2. Multi-AZ configurado
3. Encryption at rest habilitado
4. Automated backups (retention, window)
5. Parameter group (tuning)
6. Connection string en secrets manager
7. Monitoring configurado

**Criterio de completitud:**
- [ ] DB con instance type correcto
- [ ] Multi-AZ habilitado
- [ ] Encryption activo
- [ ] Backups configurados
- [ ] Connection string en secrets manager
- [ ] Solo accesible desde app servers (SG)

**Anti-patrones:**
- ❌ **Single-AZ:** Si la AZ cae, la BD cae.
- ❌ **Sin backups automáticos:** Data loss si algo sale mal.
- ❌ **Sin encryption:** Compliance violation.
- ❌ **Connection string hardcoded:** Security risk.

**Template:** `phases/06-deploy/deliverables/database-ready.md` *(pendiente)*

---

### 6.1.7 Storage Ready

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.1 Infrastructure Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | S3/MinIO |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere configurar object storage para uploads, assets, y backups.  
En VTT: un agente puede generar IaC para S3 buckets. Es altamente delegable.

**Qué es:** Object storage (S3/GCS/MinIO) configurado: buckets para file uploads, static assets, y backups. Cada bucket con encryption, lifecycle policies, CORS (si direct upload), y access policies restrictivas.

**Para qué sirve:** Storage para archivos que no van en BD: uploads, imágenes, PDFs, exports, backups. Config correcta asegura seguridad, costo controlado, y funcionalidad.

**Inputs requeridos:**
- `3B.8.1` Infrastructure Plan — storage requirements
- `3B.7.5` Encryption Strategy — encryption config

**Dependencias (predecessors):**
- `6.1.1` Infrastructure Ready *(obligatorio)*

**Habilita (successors):**
- File uploads funcionales
- Backup storage disponible

**Audiencia:**
- **DevOps Lead** — configuración
- **Backend Developer** — integración

**Secciones esperadas:**
1. Buckets creados (tabla: nombre, propósito, encryption, lifecycle)
2. Encryption configurada
3. Lifecycle policies
4. CORS configuration (si aplica)
5. Access policies (IAM roles, bucket policies)
6. Versioning

**Criterio de completitud:**
- [ ] Buckets para uploads, assets, y backups
- [ ] Encryption en todos los buckets
- [ ] Lifecycle policies configuradas
- [ ] Access policies restrictivas (no public)

**Anti-patrones:**
- ❌ **Bucket público:** Uploads accesibles por cualquiera.
- ❌ **Sin lifecycle:** Files acumulados forever — costos crecientes.
- ❌ **Sin encryption:** Compliance violation.

**Template:** `phases/06-deploy/deliverables/storage-ready.md` *(pendiente)*

---

### 6.1.8 SSL Certificates

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.1 Infrastructure Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Security Engineer |
| **Formato** | Certs |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez + auto-renewal |

**Perfil de ejecución:** Requiere provisionar certificados SSL/TLS.  
En VTT: un agente puede generar IaC para ACM certificates. Es altamente delegable.

**Qué es:** Certificados SSL/TLS provisionados (ACM/Let's Encrypt), configurados en LB para SSL termination, con auto-renewal y HSTS header habilitado.

**Para qué sirve:** HTTPS es requisito absoluto: protege datos en tránsito, requisito de SEO, y requisito de OAuth providers. Sin SSL, tráfico interceptable.

**Inputs requeridos:**
- Dominio registrado
- `6.1.5` Load Balancer — donde instalar certificado

**Dependencias (predecessors):**
- `6.1.5` Load Balancer *(obligatorio)*
- Dominio registrado *(obligatorio)*

**Habilita (successors):**
- `6.5.4` SSL Active — SSL en producción
- HTTPS funcional

**Audiencia:**
- **DevOps Lead** — provisioning
- **Security Engineer** — validación

**Secciones esperadas:**
1. Certificate provisioned (provider)
2. Domain validated
3. Configured on Load Balancer
4. Auto-renewal configurado
5. HTTP → HTTPS redirect
6. HSTS header
7. Certificate monitoring (alert before expiry)

**Criterio de completitud:**
- [ ] Certificado válido para el dominio
- [ ] Configurado en LB
- [ ] Auto-renewal funcional
- [ ] HTTP → HTTPS redirect
- [ ] HSTS configurado
- [ ] Monitoring de expiry

**Anti-patrones:**
- ❌ **Self-signed en producción:** Browser warnings.
- ❌ **Sin auto-renewal:** Expira → downtime.
- ❌ **Sin HSTS:** Permite downgrade a HTTP.

**Template:** `phases/06-deploy/deliverables/ssl-certificates.md` *(pendiente)*

---

## 6.2 CI/CD Configuration (6 deliverables)

**Responsable:** DevOps Lead | **Aprueba:** Tech Lead

---

### 6.2.1 CI Pipeline

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.2 CI/CD Configuration |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | YAML |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + mantenimiento |

**Perfil de ejecución:** Requiere experiencia con GitHub Actions, GitLab CI, o CircleCI.  
En VTT: un agente puede generar pipeline YAML completo. Es altamente delegable.

**Qué es:** Pipeline de Continuous Integration: lint → type check → unit tests → integration tests → build → coverage report. Se ejecuta en cada push/PR. Gate: si falla, PR no se puede mergear (branch protection).

**Para qué sirve:** CI asegura que cada cambio es: linted, type-checked, testeado, y buildeable. Detecta problemas antes del merge.

**Inputs requeridos:**
- `4.1.9` Linter Configuration — lint step
- `4.6.3` Test Coverage Report — coverage step
- `3B.1.5` Technology Stack — build tools

**Dependencias (predecessors):**
- `4.1.9` Linter Configuration *(obligatorio)*
- Tests configurados (4.3.9, 4.4.10) *(obligatorio)*

**Habilita (successors):**
- `6.2.2` CD Pipeline — build artifact
- Branch protection — PR gate

**Audiencia:**
- **Todo el equipo de desarrollo** — CI results en cada PR

**Secciones esperadas:**
1. Pipeline YAML (steps: lint, type-check, test, build, coverage)
2. Trigger config (on push, on PR)
3. Caching (node_modules, Docker layers)
4. Secrets injection
5. Notifications (Slack on failure)
6. Branch protection rules

**Criterio de completitud:**
- [ ] Pipeline ejecuta en cada PR
- [ ] Steps completos: lint, type-check, tests, build
- [ ] Coverage report generado
- [ ] CI falla si lint errors, tests fail, o coverage < threshold
- [ ] Caching configurado (execution < 10 min)
- [ ] Branch protection: min 1 approval + CI green

**Anti-patrones:**
- ❌ **CI de 30 min:** Developers mergean sin esperar CI.
- ❌ **Sin branch protection:** CI es opcional.
- ❌ **Secrets en YAML:** API keys commiteadas.

**Template:** `phases/06-deploy/deliverables/ci-pipeline.yml` *(pendiente)*

---

### 6.2.2 CD Pipeline

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.2 CI/CD Configuration |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | YAML |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + mantenimiento |

**Perfil de ejecución:** Requiere configurar deployment automático con health checks y rollback.  
En VTT: un agente puede generar CD pipeline YAML. Es altamente delegable.

**Qué es:** Pipeline de Continuous Deployment: build image → push registry → deploy staging (automático desde main) → deploy production (manual approval gate). Incluye migration run, health check post-deploy, y rollback automático si health check falla.

**Para qué sirve:** CD automatiza deploy para que sea reproducible, rápido (minutos), y seguro (health checks, rollback automático).

**Inputs requeridos:**
- `6.2.1` CI Pipeline — build artifact
- `6.1.1` Infrastructure Ready — target de deploy
- `6.2.4` Deploy Scripts — scripts ejecutados

**Dependencias (predecessors):**
- `6.2.1` CI Pipeline *(obligatorio)*
- `6.1.1` Infrastructure Ready *(obligatorio)*

**Habilita (successors):**
- `6.3.1` Staging Deploy — deploy automático
- `6.5.1` Production Deploy — deploy con approval

**Audiencia:**
- **DevOps Lead** — configuración
- **Tech Lead** — approval gate

**Secciones esperadas:**
1. Build step (Docker image, tag with commit SHA)
2. Push to registry
3. Deploy to staging (automático desde main)
4. Health check post-deploy
5. Manual approval gate (para producción)
6. Deploy to production
7. Rollback automático si health check falla
8. Notifications

**Criterio de completitud:**
- [ ] Deploy a staging automático desde main
- [ ] Deploy a prod con manual approval
- [ ] Health check post-deploy
- [ ] Rollback automático si health check falla
- [ ] Migration run incluido
- [ ] Notifications configuradas
- [ ] Execution < 10 min

**Anti-patrones:**
- ❌ **Deploy manual:** SSH + git pull — no reproducible.
- ❌ **Sin health check post-deploy:** App crasheando sin detectar.
- ❌ **Sin approval gate:** Auto-deploy a producción sin human check.

**Template:** `phases/06-deploy/deliverables/cd-pipeline.yml` *(pendiente)*

---

### 6.2.3 Build Scripts

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.2 CI/CD Configuration |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Shell |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + mantenimiento |

**Perfil de ejecución:** Requiere scripts de build parametrizables por environment.  
En VTT: un agente puede generar build scripts. Es altamente delegable.

**Qué es:** Scripts de build: compilan código, bundlean assets, generan Docker image, y producen artifact deployable. Parametrizables por environment (source maps en dev, minification en prod).

**Para qué sirve:** Build reproducible y automatizado asegura que lo deployado es lo testeado.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — build tools
- `4.1.4` Docker Compose — Dockerfile de producción

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)*

**Habilita (successors):**
- `6.2.1` CI Pipeline — build step
- `6.2.2` CD Pipeline — build step

**Audiencia:**
- **DevOps Lead** — mantenimiento
- **Developers** — build local

**Secciones esperadas:**
1. Build script (build.sh o Makefile target)
2. Dockerfile de producción (multi-stage)
3. Environment-specific config (build args)
4. Build output (Docker image, tag strategy)

**Criterio de completitud:**
- [ ] Build genera artifact deployable
- [ ] Reproducible
- [ ] Parametrizable por environment
- [ ] Build time < 5 min
- [ ] Multi-stage Dockerfile

**Anti-patrones:**
- ❌ **Build no-reproducible:** Local ≠ CI.
- ❌ **Sin multi-stage:** Imagen con devDependencies — pesada e insegura.

**Template:** `phases/06-deploy/deliverables/build-scripts.sh` *(pendiente)*

---

### 6.2.4 Deploy Scripts

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.2 CI/CD Configuration |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Shell |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + mantenimiento |

**Perfil de ejecución:** Requiere scripts con migration, health check, y rollback.  
En VTT: un agente puede generar deploy scripts. Es altamente delegable.

**Qué es:** Scripts de deploy: push image, run migrations, deploy nueva versión (rolling update o blue-green), verify health, y rollback si falla. Incluye deploy.sh, rollback.sh, y migrate.sh.

**Para qué sirve:** Bajo presión (deploy fallido a las 3AM), el script ejecuta los pasos correctos sin errores humanos.

**Inputs requeridos:**
- `6.1.1` Infrastructure Ready — target
- `6.2.3` Build Scripts — artifact

**Dependencias (predecessors):**
- `6.2.3` Build Scripts *(obligatorio)*
- `6.1.1` Infrastructure Ready *(obligatorio)*

**Habilita (successors):**
- `6.3.1` Staging Deploy — deploy execution
- `6.5.1` Production Deploy — deploy execution

**Audiencia:**
- **DevOps Lead** — ejecución

**Secciones esperadas:**
1. deploy.sh (push, migrate, deploy, health check)
2. rollback.sh (revert to previous version)
3. migrate.sh (run migrations with safety checks)
4. Health check verification

**Criterio de completitud:**
- [ ] Deploy script funcional end-to-end
- [ ] Rollback script funcional y probado
- [ ] Migration script con safety checks
- [ ] Health check post-deploy incluido

**Anti-patrones:**
- ❌ **Sin rollback script:** Si falla, no hay reversión automatizada.
- ❌ **Scripts sin error handling:** Un step falla pero continúa — deploy parcial.

**Template:** `phases/06-deploy/deliverables/deploy-scripts.sh` *(pendiente)*

---

### 6.2.5 Environment Configs

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.2 CI/CD Configuration |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | YAML |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + por environment |

**Perfil de ejecución:** Requiere configuración por ambiente sin secrets hardcoded.  
En VTT: un agente puede generar env configs. Es altamente delegable.

**Qué es:** Config files por environment (dev, staging, prod): variables que difieren entre ambientes (API URLs, feature flags, log levels, DB hostnames), separadas de secrets. Cada environment tiene su config que se inyecta durante deploy.

**Para qué sirve:** Misma app + diferente config = diferente comportamiento por ambiente. Sin configs separadas, se usa la misma config everywhere — test keys en producción.

**Inputs requeridos:**
- `3B.8.5` Environment Matrix — ambientes definidos
- `4.1.3` Environment Variables — variables por ambiente

**Dependencias (predecessors):**
- `3B.8.5` Environment Matrix *(obligatorio)*
- `4.1.3` Environment Variables *(obligatorio)*

**Habilita (successors):**
- Deploy correcto por ambiente

**Audiencia:**
- **DevOps Lead** — configuración
- **Developers** — entender diferencias por ambiente

**Secciones esperadas:**
1. Config file por ambiente (dev.yml, staging.yml, prod.yml)
2. Variables que difieren (tabla: variable, dev, staging, prod)
3. Secrets excluidos (referencia a secrets manager)
4. Feature flags por ambiente

**Criterio de completitud:**
- [ ] Config por ambiente (dev, staging, prod)
- [ ] Sin secrets en config files
- [ ] Feature flags diferenciados
- [ ] Configs versionadas en repo

**Anti-patrones:**
- ❌ **Secrets en configs:** DB password commiteado.
- ❌ **Misma config everywhere:** Debug en producción.

**Template:** `phases/06-deploy/deliverables/environment-configs/` *(pendiente)*

---

### 6.2.6 Pipeline Documentation

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.2 CI/CD Configuration |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + actualizaciones |

**Perfil de ejecución:** Requiere documentar pipelines para que cualquier developer pueda operarlos.  
En VTT: un agente puede generar la documentación. Es altamente delegable.

**Qué es:** Documentación de pipelines CI/CD: qué hace cada step, cómo triggerar deploy, cómo hacer rollback, cómo agregar un step, y troubleshooting de failures comunes.

**Para qué sirve:** Sin docs, solo DevOps sabe cómo funciona. Con docs, cualquier developer puede: entender CI failures, triggerar deploy, y hacer rollback.

**Inputs requeridos:**
- `6.2.1` CI Pipeline — pipeline a documentar
- `6.2.2` CD Pipeline — pipeline a documentar

**Dependencias (predecessors):**
- `6.2.1` CI Pipeline *(obligatorio)*
- `6.2.2` CD Pipeline *(obligatorio)*

**Habilita (successors):**
- Autonomía del equipo para operar CI/CD

**Audiencia:**
- **Todo el equipo de desarrollo**

**Secciones esperadas:**
1. CI: qué hace cada step, triggers, cómo leer failures
2. CD: cómo triggear deploy, approval process, rollback
3. Troubleshooting de errores comunes
4. Cómo agregar un step
5. Secrets management en pipelines

**Criterio de completitud:**
- [ ] CI y CD documentados step-by-step
- [ ] Cómo triggear deploy y rollback
- [ ] Troubleshooting 3+ problemas comunes
- [ ] Probado por developer que no lo escribió

**Anti-patrones:**
- ❌ **Sin docs:** Solo DevOps sabe — bus factor 1.

**Template:** `phases/06-deploy/deliverables/pipeline-docs.md` *(pendiente)*

---

## 6.3 Staging Deploy (4 deliverables)

**Responsable:** DevOps Lead | **Aprueba:** Tech Lead

---

### 6.3.1 Staging Deploy

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.3 Staging Deploy |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead (automático via CD) |
| **Aprueba** | Tech Lead |
| **Formato** | Log |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Automático (15 min) |
| **Frecuencia** | Por merge a main |

**Perfil de ejecución:** Requiere CD pipeline funcional.  
En VTT: N/A — ejecutado automáticamente por CD pipeline.

**Qué es:** Deploy exitoso a staging: código deployed, migrations aplicadas, servicios corriendo, health checks pasando. Evidenciado por deploy log y URL accesible.

**Para qué sirve:** Staging es el "ensayo general" antes de producción. QA y PO validan aquí.

**Inputs requeridos:**
- `6.2.2` CD Pipeline — ejecuta deploy
- `6.1.1` Infrastructure Ready — staging environment
- Código en main branch

**Dependencias (predecessors):**
- `6.2.2` CD Pipeline *(obligatorio)*
- `6.1.1` Infrastructure Ready *(obligatorio)*

**Habilita (successors):**
- `6.3.4` Health Check — verificación
- `6.4.1` Smoke Test Results — smoke test en staging

**Audiencia:**
- **DevOps Lead** — verificación
- **QA Team** — ambiente para testing
- **Product Owner** — preview

**Secciones esperadas:**
1. Deploy log (timestamp, version, status)
2. Services running (backend, frontend, workers)
3. Migration status
4. Health check results

**Criterio de completitud:**
- [ ] Deploy exitoso sin errors
- [ ] Todos los services corriendo
- [ ] Migrations aplicadas
- [ ] Health checks: 200 OK
- [ ] URL accesible

**Anti-patrones:**
- ❌ **Deploy sin verificar:** "Lo deployé" sin confirmar que funciona.

**Template:** `phases/06-deploy/deliverables/staging-deploy-log.md` *(pendiente)*

---

### 6.3.2 Staging URL

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.3 Staging Deploy |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | URL |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere DNS configurado para staging.  
En VTT: un agente puede configurar DNS. Es altamente delegable.

**Qué es:** URL accesible de staging (staging.app.com): frontend y backend accesibles, con SSL, compartida con QA, PO, y stakeholders.

**Para qué sirve:** QA y PO necesitan URL estable para testing y preview.

**Inputs requeridos:**
- `6.3.1` Staging Deploy — app deployed
- DNS configurado

**Dependencias (predecessors):**
- `6.3.1` Staging Deploy *(obligatorio)*

**Habilita (successors):**
- QA testing y PO preview en staging

**Audiencia:**
- **Todo el equipo** — acceso a staging

**Secciones esperadas:**
1. Frontend URL
2. Backend API URL
3. Swagger URL
4. Test credentials

**Criterio de completitud:**
- [ ] URL accesible y funcional
- [ ] SSL configurado
- [ ] Compartida con el equipo
- [ ] Test credentials documentadas

**Anti-patrones:**
- ❌ **URL que cambia:** IP variable — usar DNS.

**Template:** N/A — URL documentada en README

---

### 6.3.3 Migration Run

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.3 Staging Deploy |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Log |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Automático |
| **Frecuencia** | Por deploy |

**Perfil de ejecución:** Requiere migrations ejecutadas como parte del deploy.  
En VTT: N/A — automático via deploy scripts.

**Qué es:** Ejecución de database migrations en staging: pending migrations aplicadas, schema actualizado, verificación de estado correcto. Log de migrations como evidencia.

**Para qué sirve:** Sin migration run, código nuevo espera columnas que no existen — errors en runtime.

**Inputs requeridos:**
- `4.2.2` Schema Migrations — migrations pendientes
- `6.2.4` Deploy Scripts — migration step

**Dependencias (predecessors):**
- `6.3.1` Staging Deploy *(co-dependencia)*

**Habilita (successors):**
- App funcional con schema correcto

**Audiencia:**
- **DevOps Lead** — verificación
- **Database Engineer** — validación

**Secciones esperadas:**
1. Migration log (cuáles ejecutadas, status)
2. Schema verification
3. Rollback status

**Criterio de completitud:**
- [ ] Pending migrations aplicadas
- [ ] 0 errors en log
- [ ] Schema coincide con el esperado

**Anti-patrones:**
- ❌ **Migrations que fallan silenciosamente:** "Success" pero datos inconsistentes.

**Template:** N/A — log automático

---

### 6.3.4 Health Check

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.3 Staging Deploy |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Por deploy |

**Perfil de ejecución:** Requiere verificar todos los componentes post-deploy.  
En VTT: un agente puede ejecutar health checks automatizados. Es altamente delegable.

**Qué es:** Verificación post-deploy: API endpoints responden (GET /health → 200), BD accesible, cache accesible, servicios externos conectados, y performance baseline. El "chequeo médico" post-deploy.

**Para qué sirve:** Deploy puede ser "exitoso" pero app puede estar rota (config incorrecta, migration rompió datos). Health check verifica end-to-end.

**Inputs requeridos:**
- `6.3.1` Staging Deploy — app deployed
- Health check endpoints

**Dependencias (predecessors):**
- `6.3.1` Staging Deploy *(obligatorio)*
- `6.3.3` Migration Run *(obligatorio)*

**Habilita (successors):**
- `6.4.1` Smoke Test Results — si health pasa, QA procede

**Audiencia:**
- **DevOps Lead** — verificación
- **Tech Lead** — go/no-go
- **QA Lead** — puede empezar testing

**Secciones esperadas:**
1. API health endpoint (200 con status de dependencies)
2. Database connectivity
3. Cache connectivity
4. External services
5. Basic performance check
6. Overall: HEALTHY / DEGRADED / UNHEALTHY

**Criterio de completitud:**
- [ ] API health: 200
- [ ] BD accesible
- [ ] Cache accesible
- [ ] External services conectados
- [ ] Overall: HEALTHY

**Anti-patrones:**
- ❌ **Health check que solo checa "app is running":** No verifica BD, cache — false positive.
- ❌ **Health check que siempre retorna 200:** No checa nada realmente.

**Template:** `phases/06-deploy/deliverables/health-check.md` *(pendiente)*

---

## 6.4 Smoke Testing (3 deliverables)

**Responsable:** QA Engineer | **Aprueba:** QA Lead

---

### 6.4.1 Smoke Test Results

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.4 Smoke Testing |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | QA Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Por deploy |

**Perfil de ejecución:** Requiere tests rápidos (15-30 min) de funcionalidades principales.  
En VTT: un agente puede ejecutar E2E subset automatizado. Es parcialmente delegable.

**Qué es:** Resultados de smoke testing post-deploy: tests rápidos que verifican funcionalidades principales. No es testing exhaustivo — es verificación de que el deploy no rompió nada crítico: login, CRUD principal, navegación, y integración con servicios críticos.

**Para qué sirve:** Deploy puede romper cosas inesperadas. Smoke test detecta problemas críticos rápidamente — antes de que usuarios los encuentren.

**Inputs requeridos:**
- Deploy completado (6.3.1 o 6.5.1)
- `5.6.1` E2E Test Suite — subset para smoke

**Dependencias (predecessors):**
- `6.3.4` Health Check *(obligatorio)*

**Habilita (successors):**
- `6.4.3` Smoke Test Sign-off — aprobación

**Audiencia:**
- **QA Engineer** — ejecución
- **QA Lead** — aprobación

**Secciones esperadas:**
1. Tests ejecutados (tabla: test, resultado, duración)
2. Flujos verificados
3. Issues encontrados
4. Overall: PASS / FAIL

**Criterio de completitud:**
- [ ] 3-5 flujos críticos verificados
- [ ] No hay blockers
- [ ] Ejecutado en < 30 min

**Anti-patrones:**
- ❌ **Smoke test de 4 horas:** Eso es regression — smoke = 15-30 min.
- ❌ **Skip smoke:** Health check ≠ funcionalidad verificada.

**Template:** `phases/06-deploy/deliverables/smoke-test-results.md` *(pendiente)*

---

### 6.4.2 Critical Paths Verified

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.4 Smoke Testing |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | QA Lead |
| **Formato** | Checklist |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en 6.4.1 |
| **Frecuencia** | Por deploy |

**Perfil de ejecución:** Requiere verificar flujos críticos manualmente.  
En VTT: un agente puede generar checklist. NO puede ejecutar verificación manual.

**Qué es:** Checklist de flujos críticos verificados: cada flujo marcado ✅/❌. Flujos críticos = los que si fallan, el producto es inutilizable: login/auth, CRUD principal, pago (si aplica), navegación, búsqueda.

**Para qué sirve:** Evidencia formal de que se verificó cada flujo crítico. Asegura que no se olvida ninguno.

**Inputs requeridos:**
- `2.6.2` Happy Path Flows — flujos críticos
- `6.4.1` Smoke Test Results

**Dependencias (predecessors):**
- `6.4.1` Smoke Test Results *(co-dependencia)*

**Habilita (successors):**
- `6.4.3` Smoke Test Sign-off — evidencia

**Audiencia:**
- **QA Lead** — verificación de coverage

**Secciones esperadas:**
1. Checklist (flujo, status ✅/❌, notas)
2. Fecha y versión
3. Tester

**Criterio de completitud:**
- [ ] Todos los flujos críticos verificados
- [ ] 0 flujos con ❌ para proceder a prod

**Anti-patrones:**
- ❌ **Auto-check sin verificar:** Marcar ✅ sin testear — teatro.

**Template:** `phases/06-deploy/deliverables/critical-paths-checklist.md` *(pendiente)*

---

### 6.4.3 Smoke Test Sign-off

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.4 Smoke Testing |
| **Responsable** | QA Lead |
| **Ejecuta** | QA Lead |
| **Aprueba** | QA Lead |
| **Formato** | Sign-off |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Por deploy |

**Perfil de ejecución:** Requiere autoridad del QA Lead para go/no-go.  
En VTT: un agente puede compilar sign-off document. NO puede tomar decisión.

**Qué es:** Aprobación formal de QA Lead: smoke tests pasaron, flujos críticos verificados, no hay blockers, riesgo residual aceptable.

**Para qué sirve:** Gate entre staging y producción. Sin sign-off de QA, no se deploya a prod.

**Inputs requeridos:**
- `6.4.1` Smoke Test Results
- `6.4.2` Critical Paths Verified

**Dependencias (predecessors):**
- `6.4.1` Smoke Test Results *(obligatorio)*
- `6.4.2` Critical Paths Verified *(obligatorio)*

**Habilita (successors):**
- `6.5.1` Production Deploy — gate de entrada

**Audiencia:**
- **QA Lead** — decisor
- **Tech Lead** — coordinación

**Secciones esperadas:**
1. Results summary
2. Critical paths: all ✅
3. Known issues
4. Go/No-go decision
5. Signature

**Criterio de completitud:**
- [ ] Smoke tests ejecutados
- [ ] Critical paths todos ✅
- [ ] Decision documentada
- [ ] Firmado por QA Lead

**Anti-patrones:**
- ❌ **Sign-off sin smoke test:** Aprobar sin testear.
- ❌ **Sign-off con blocker:** Proceder con flujo crítico roto.

**Template:** `phases/06-deploy/deliverables/smoke-test-signoff.md` *(pendiente)*

---

## 6.5 Production Deploy (6 deliverables)

**Responsable:** DevOps Lead | **Aprueba:** Product Owner

---

### 6.5.1 Production Deploy

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.5 Production Deploy |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Product Owner |
| **Formato** | Log |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Por release |

**Perfil de ejecución:** Requiere ejecutar CD pipeline con approval gate.  
En VTT: N/A — ejecutado por CD pipeline con human approval.

**Qué es:** Deploy exitoso a producción. El producto está live para usuarios reales. Ejecutado vía CD pipeline con manual approval. Incluye pre-deploy checklist, deploy execution, post-deploy health check, y smoke test en prod.

**Para qué sirve:** Culmination de todo el trabajo. Deploy bien ejecutado es planificado, verificado, y reversible.

**Inputs requeridos:**
- `6.4.3` Smoke Test Sign-off — QA aprobó
- `5.10.5` UAT Sign-off — PO aprobó
- `6.7.1` Rollback Plan — rollback listo

**Dependencias (predecessors):**
- `6.4.3` Smoke Test Sign-off *(obligatorio)*
- `5.10.5` UAT Sign-off *(obligatorio)*
- `5.8.7` Security Sign-off *(obligatorio)*
- `6.7.3` Rollback Tested *(obligatorio)*

**Habilita (successors):**
- `6.5.2` a `6.5.6` — post-deploy deliverables
- `6.6.1` Monitoring Dashboard — monitoring activo
- Producto live

**Audiencia:**
- **Product Owner** — approval
- **DevOps Lead** — execution
- **Tech Lead** — coordination
- **On-call team** — standby

**Secciones esperadas:**
1. Pre-deploy checklist (backup, rollback, on-call, comms)
2. Deploy execution log (timestamp, version, steps, status)
3. Post-deploy health check
4. Post-deploy smoke test
5. Overall: SUCCESS / ROLLBACK

**Criterio de completitud:**
- [ ] Pre-deploy checklist completado
- [ ] Deploy sin errores
- [ ] Health check: HEALTHY
- [ ] Smoke test: PASS
- [ ] 0 errors críticos post-deploy
- [ ] On-call notificado

**Anti-patrones:**
- ❌ **Deploy viernes 6PM:** Sin equipo si falla.
- ❌ **Sin backup previo:** Sin recovery si migration corrompe datos.
- ❌ **Sin rollback plan:** Caos si falla.

**Template:** `phases/06-deploy/deliverables/production-deploy.md` *(pendiente)*

---

### 6.5.2 Production URL

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.5 Production Deploy |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Product Owner |
| **Formato** | URL |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Verificación de URL accesible.  
En VTT: N/A — verificación simple.

**Qué es:** URL de producción (app.com) verificada: frontend carga, API responde, SSL activo, performance aceptable.

**Para qué sirve:** Confirmación de que el producto está accesible para el público.

**Inputs requeridos:**
- `6.5.1` Production Deploy
- `6.5.3` DNS Configured

**Dependencias (predecessors):**
- `6.5.1` Production Deploy *(obligatorio)*
- `6.5.3` DNS Configured *(obligatorio)*

**Habilita (successors):**
- Marketing y comunicación del launch

**Audiencia:**
- **Todos**

**Secciones esperadas:**
1. Production URL
2. API URL
3. Status page URL

**Criterio de completitud:**
- [ ] URL accesible públicamente
- [ ] Frontend sin errores
- [ ] API responde
- [ ] SSL activo
- [ ] Performance < 3s page load

**Anti-patrones:**
- ❌ **Mixed content warnings:** HTTP resources en HTTPS page.

**Template:** N/A

---

### 6.5.3 DNS Configured

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.5 Production Deploy |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Config |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere configurar DNS records apuntando al LB.  
En VTT: un agente puede generar IaC para DNS. Es altamente delegable.

**Qué es:** DNS configurado: A/CNAME records apuntando al LB, propagation verificada, TTL configurado. Incluye dominio principal, www redirect, y API subdomain.

**Para qué sirve:** Sin DNS, usuarios accederían por IP — imposible.

**Inputs requeridos:**
- `6.1.5` Load Balancer — target del DNS
- Dominio registrado

**Dependencias (predecessors):**
- `6.1.5` Load Balancer *(obligatorio)*

**Habilita (successors):**
- `6.5.2` Production URL

**Audiencia:**
- **DevOps Lead**

**Secciones esperadas:**
1. DNS records (tabla: type, name, value, TTL)
2. Propagation verification
3. www redirect
4. API subdomain

**Criterio de completitud:**
- [ ] A/CNAME apuntando al LB
- [ ] Propagation verificada
- [ ] www → apex redirect
- [ ] TTL razonable

**Anti-patrones:**
- ❌ **TTL 86400s:** Cambios tardan 24h en propagarse.
- ❌ **Sin verificar propagación:** DNS configurado pero no funciona.

**Template:** N/A

---

### 6.5.4 SSL Active

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.5 Production Deploy |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Security Engineer |
| **Formato** | Verificación |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido |
| **Frecuencia** | Una vez + monitoring |

**Perfil de ejecución:** Verificar SSL correcto en producción.  
En VTT: un agente puede verificar SSL automáticamente. Es altamente delegable.

**Qué es:** Verificación: certificado válido, HTTPS funcional, HTTP → HTTPS redirect, HSTS activo, SSL Labs grade A+.

**Para qué sirve:** HTTPS mal configurado = datos en plain text, browser warnings, SEO penalty, y OAuth failures.

**Inputs requeridos:**
- `6.1.8` SSL Certificates
- `6.5.2` Production URL

**Dependencias (predecessors):**
- `6.1.8` SSL Certificates *(obligatorio)*
- `6.5.1` Production Deploy *(obligatorio)*

**Habilita (successors):**
- Producto seguro para usuarios

**Audiencia:**
- **Security Engineer** — validación

**Secciones esperadas:**
1. Certificate validity
2. HTTPS functional
3. HTTP → HTTPS redirect
4. HSTS header
5. SSL Labs grade

**Criterio de completitud:**
- [ ] Certificado válido
- [ ] HTTPS funcional
- [ ] Redirect activo
- [ ] HSTS configurado
- [ ] SSL Labs: A o A+

**Anti-patrones:**
- ❌ **SSL sin HSTS:** Permite downgrade a HTTP.
- ❌ **Mixed content:** HTTPS page con HTTP resources.

**Template:** N/A

---

### 6.5.5 Release Notes

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.5 Production Deploy |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead / Technical Writer |
| **Aprueba** | Product Owner |
| **Formato** | MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Por release |

**Perfil de ejecución:** Requiere traducir changelog técnico en notas para usuarios.  
En VTT: un agente puede generar release notes desde changelog. Es altamente delegable.

**Qué es:** Notas de release para usuarios/stakeholders: qué hay de nuevo, qué cambió, qué se arregló. Lenguaje no-técnico, con screenshots. Derivadas del Changelog (4.7.8).

**Para qué sirve:** Usuarios y stakeholders necesitan saber qué cambió. Sin release notes, soporte recibe preguntas evitables.

**Inputs requeridos:**
- `4.7.8` Changelog — cambios técnicos

**Dependencias (predecessors):**
- `4.7.8` Changelog *(obligatorio)*

**Habilita (successors):**
- Comunicación de launch
- User awareness

**Audiencia:**
- **Users** — qué hay de nuevo
- **Product Owner** — validación
- **Marketing** — material de comunicación

**Secciones esperadas:**
1. Version y fecha
2. Highlights (top 3)
3. New features (con screenshots)
4. Improvements
5. Bug fixes (relevantes para usuario)
6. Breaking changes (si hay)
7. Known issues

**Criterio de completitud:**
- [ ] Cambios visibles documentados
- [ ] Lenguaje no-técnico
- [ ] Screenshots de features nuevas
- [ ] Aprobado por Product Owner

**Anti-patrones:**
- ❌ **Release notes técnicas:** "Fixed N+1 query" — el usuario no entiende.
- ❌ **Sin release notes:** Usuarios descubren cambios por sorpresa.

**Template:** `phases/06-deploy/deliverables/release-notes.md` *(pendiente)*

---

### 6.5.6 Deployment Log

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.5 Production Deploy |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Log |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido |
| **Frecuencia** | Por deploy |

**Perfil de ejecución:** Registro del deployment para auditoría.  
En VTT: un agente puede compilar el log. Es altamente delegable.

**Qué es:** Registro detallado: timestamp inicio/fin, versión (commit SHA, tag), quién deployó, steps con status, issues durante deploy, tiempo total.

**Para qué sirve:** Cuando algo sale mal post-deploy, el log dice: qué versión, cuándo, quién, y si hubo issues durante el deploy.

**Inputs requeridos:**
- `6.5.1` Production Deploy

**Dependencias (predecessors):**
- `6.5.1` Production Deploy *(co-dependencia)*

**Habilita (successors):**
- Auditoría y post-mortem

**Audiencia:**
- **DevOps Lead** — record
- **Tech Lead** — auditoría

**Secciones esperadas:**
1. Timestamp inicio/fin
2. Version (SHA, tag)
3. Deployer
4. Steps con status
5. Issues
6. Tiempo total
7. Post-deploy status

**Criterio de completitud:**
- [ ] Timestamp registrado
- [ ] Version documentada
- [ ] Steps con status
- [ ] Overall result
- [ ] Archivado

**Anti-patrones:**
- ❌ **Sin log:** Nadie recuerda qué, cuándo, quién.

**Template:** `phases/06-deploy/deliverables/deployment-log.md` *(pendiente)*

---

## 6.6 Post-Deploy Monitoring (6 deliverables)

**Responsable:** SRE | **Aprueba:** Tech Lead

---

### 6.6.1 Monitoring Dashboard

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.6 Post-Deploy Monitoring |
| **Responsable** | SRE |
| **Ejecuta** | SRE |
| **Aprueba** | Tech Lead |
| **Formato** | Grafana/Datadog |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + evolución |

**Perfil de ejecución:** Requiere crear dashboards con métricas clave.  
En VTT: un agente puede generar dashboard configs. Es bastante delegable.

**Qué es:** Dashboard de monitoring en tiempo real: request rate, error rate, latency (p50/p95/p99), CPU/RAM, DB connections, cache hit rate, y business metrics. Visible para equipo técnico.

**Para qué sirve:** Sin dashboard, nadie sabe cómo está el sistema hasta que un usuario se queja. Con dashboard, el equipo ve problemas en tiempo real.

**Inputs requeridos:**
- `3B.8.11` Monitoring Strategy — métricas
- `6.6.4` Metrics Collection — data source

**Dependencias (predecessors):**
- `6.5.1` Production Deploy *(obligatorio)*
- `6.6.4` Metrics Collection *(obligatorio)*

**Habilita (successors):**
- `7.1.1` Uptime Reports — datos del dashboard
- Detección proactiva de problemas

**Audiencia:**
- **SRE** — monitoring diario
- **Tech Lead** — health overview

**Secciones esperadas:**
1. Overview panel (request rate, error rate, latency, uptime)
2. Infrastructure panel (CPU, RAM, disk)
3. Database panel (connections, query time)
4. Application panel (per-endpoint metrics)
5. Business panel (signups, orders)
6. SLO compliance panel

**Criterio de completitud:**
- [ ] Dashboard creado y accesible
- [ ] Métricas clave visibles
- [ ] SLO targets marcados
- [ ] Auto-refresh
- [ ] Accesible por equipo técnico

**Anti-patrones:**
- ❌ **50 panels:** Demasiada información — priorizar métricas críticas.

**Template:** `phases/06-deploy/deliverables/monitoring-dashboard.json` *(pendiente)*

---

### 6.6.2 Alerts Configured

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.6 Post-Deploy Monitoring |
| **Responsable** | SRE |
| **Ejecuta** | SRE |
| **Aprueba** | Tech Lead |
| **Formato** | Config |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + tuning |

**Perfil de ejecución:** Requiere configurar alertas con thresholds correctos.  
En VTT: un agente puede generar alert configs. Es altamente delegable.

**Qué es:** Alertas para condiciones críticas: error rate > 1%, latency p95 > 500ms, CPU > 80%, disk > 90%, health check failure, SSL near expiry. Notifications a Slack/PagerDuty. Cada alerta con runbook link.

**Para qué sirve:** Alertas detectan problemas antes de que usuarios los reporten.

**Inputs requeridos:**
- `3B.8.11` Monitoring Strategy
- `6.6.1` Monitoring Dashboard

**Dependencias (predecessors):**
- `6.6.1` Monitoring Dashboard *(obligatorio)*

**Habilita (successors):**
- Detección automática de problemas

**Audiencia:**
- **SRE** — recibe alertas
- **On-call team** — response

**Secciones esperadas:**
1. Alert rules (tabla: name, condition, threshold, severity, channel, runbook)
2. Notification channels
3. Severity levels
4. Runbook link per alert
5. Test alerts verified

**Criterio de completitud:**
- [ ] Alertas para: error rate, latency, CPU, disk, health check, SSL
- [ ] Notifications configuradas
- [ ] Runbook link en cada alerta
- [ ] Test alerts verificados
- [ ] No más de 10-15 alertas

**Anti-patrones:**
- ❌ **Alertas sin probar:** No funcionan durante outage real.
- ❌ **50 alertas:** Alert fatigue.
- ❌ **Sin runbook:** Alerta dispara pero nadie sabe qué hacer.

**Template:** `phases/06-deploy/deliverables/alerts-config.yml` *(pendiente)*

---

### 6.6.3 Log Aggregation

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.6 Post-Deploy Monitoring |
| **Responsable** | SRE |
| **Ejecuta** | SRE |
| **Aprueba** | Tech Lead |
| **Formato** | ELK/Loki |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere configurar log aggregation centralizada.  
En VTT: un agente puede generar config. Es bastante delegable.

**Qué es:** Logs centralizados en ELK/Loki/CloudWatch: todos los services envían logs, searchable, filterable, con retention policy. Structured JSON para parsing automático.

**Para qué sirve:** Sin aggregation, debugging requiere SSH a cada server y grep manual — imposible en clusters.

**Inputs requeridos:**
- `4.3.15` Logging — formato de logs
- `3B.8.11` Monitoring Strategy — herramienta

**Dependencias (predecessors):**
- `6.5.1` Production Deploy *(obligatorio)*
- `4.3.15` Logging *(obligatorio)*

**Habilita (successors):**
- Debugging en producción
- `7.1.3` Error Reports

**Audiencia:**
- **SRE** — debugging
- **Backend Developer** — debugging

**Secciones esperadas:**
1. Log aggregation tool configurado
2. Log shipping de todos los services
3. Structured JSON parsing
4. Search y filter
5. Retention policy

**Criterio de completitud:**
- [ ] Todos los services envían logs
- [ ] Searchable por requestId, userId, level
- [ ] Retention policy configurada
- [ ] Dashboard de logs accesible

**Anti-patrones:**
- ❌ **Logs solo en cada server:** SSH + grep — no escala.
- ❌ **Sin retention:** Costos infinitos de storage.

**Template:** `phases/06-deploy/deliverables/log-aggregation.yml` *(pendiente)*

---

### 6.6.4 Metrics Collection

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.6 Post-Deploy Monitoring |
| **Responsable** | SRE |
| **Ejecuta** | SRE |
| **Aprueba** | Tech Lead |
| **Formato** | Prometheus/CloudWatch |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + adiciones |

**Perfil de ejecución:** Requiere configurar metrics collection de infra y app.  
En VTT: un agente puede generar config. Es bastante delegable.

**Qué es:** Sistema de métricas: infraestructura (CPU, RAM, disk), aplicación (request count, duration, errors), y base de datos (connections, query time). Almacenadas en Prometheus/CloudWatch/Datadog.

**Para qué sirve:** Métricas son la base de dashboards y alertas — sin ellas, no hay observabilidad.

**Inputs requeridos:**
- `3B.8.11` Monitoring Strategy
- `4.3.15` Logging — custom metrics

**Dependencias (predecessors):**
- `6.5.1` Production Deploy *(obligatorio)*

**Habilita (successors):**
- `6.6.1` Monitoring Dashboard — data source
- `6.6.2` Alerts — conditions

**Audiencia:**
- **SRE**

**Secciones esperadas:**
1. Infrastructure metrics
2. Application metrics
3. Database metrics
4. Custom business metrics
5. Collection tool y config
6. Scrape interval

**Criterio de completitud:**
- [ ] Infra metrics recolectadas
- [ ] App metrics recolectadas
- [ ] DB metrics recolectadas
- [ ] Datos accesibles para dashboards
- [ ] Collection interval 15-60s

**Anti-patrones:**
- ❌ **Solo infra metrics:** CPU bien pero app retorna 500s — no detectado.

**Template:** `phases/06-deploy/deliverables/metrics-collection.yml` *(pendiente)*

---

### 6.6.5 Error Tracking

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.6 Post-Deploy Monitoring |
| **Responsable** | SRE |
| **Ejecuta** | SRE |
| **Aprueba** | Tech Lead |
| **Formato** | Sentry |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere configurar Sentry con source maps y release tracking.  
En VTT: un agente puede generar config de Sentry. Es altamente delegable.

**Qué es:** Sentry/Bugsnag configurado: captura errores con stack trace, user context, breadcrumbs, release tracking, y source maps. Alertas de nuevos errores y spikes.

**Para qué sirve:** Error tracking agrupa errores por impacto: "este error afecta 500 usuarios, empezó con v1.3.2, solo en Safari". Prioriza fixes por impacto real.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — Sentry SDK
- `6.5.1` Production Deploy

**Dependencias (predecessors):**
- `6.5.1` Production Deploy *(obligatorio)*

**Habilita (successors):**
- `7.1.3` Error Reports
- `7.3.3` Bug Tracking

**Audiencia:**
- **Developers** — debugging
- **SRE** — error monitoring

**Secciones esperadas:**
1. Sentry project (backend + frontend)
2. SDK configurado
3. Source maps uploaded
4. Release tracking
5. Alert rules (new error, spike)
6. User context capturado

**Criterio de completitud:**
- [ ] Sentry capturando errores BE y FE
- [ ] Source maps funcionales
- [ ] Release tracking activo
- [ ] Alerts configuradas
- [ ] User context capturado

**Anti-patrones:**
- ❌ **Sin source maps:** Stack trace minificado — imposible debuggear.
- ❌ **Sin release tracking:** No se sabe si el error es nuevo o viejo.

**Template:** `phases/06-deploy/deliverables/error-tracking.md` *(pendiente)*

---

### 6.6.6 Post-Deploy Report (24h)

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.6 Post-Deploy Monitoring |
| **Responsable** | SRE |
| **Ejecuta** | SRE |
| **Aprueba** | Tech Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Por deploy a producción |

**Perfil de ejecución:** Requiere compilar métricas de las primeras 24h.  
En VTT: un agente puede generar el reporte desde dashboards. Es altamente delegable.

**Qué es:** Reporte de las primeras 24h en producción: performance (latency, error rate, throughput), errores encontrados, incidentes (si hubo), feedback de usuarios, y overall health. El "parte médico" post-lanzamiento.

**Para qué sirve:** Las primeras 24h son las más críticas. El reporte confirma estabilidad o identifica problemas tempranos.

**Inputs requeridos:**
- `6.6.1` Monitoring Dashboard — métricas
- `6.6.5` Error Tracking — errores
- `7.2.2` Ticket System — reportes de usuarios

**Dependencias (predecessors):**
- `6.5.1` Production Deploy *(obligatorio)* — 24h después

**Habilita (successors):**
- Decisión de continuar o rollback
- `7.1.4` Weekly Reports — primer data point

**Audiencia:**
- **Tech Lead** — health
- **Product Owner** — estado
- **Management** — launch status

**Secciones esperadas:**
1. Performance metrics 24h (latency, error rate, throughput)
2. Errors detected (new, count, severity)
3. Incidents (if any)
4. User feedback / support tickets
5. Resource utilization
6. Comparison vs staging
7. Overall: HEALTHY / ISSUES / CRITICAL
8. Action items

**Criterio de completitud:**
- [ ] Métricas de 24h recolectadas
- [ ] Errores documentados
- [ ] Incidentes documentados (si hubo)
- [ ] Overall health assessment
- [ ] Compartido con stakeholders

**Anti-patrones:**
- ❌ **Sin reporte:** "Parece que funciona" — no es assessment.
- ❌ **Reporte 1 semana después:** Demasiado tarde.

**Template:** `phases/06-deploy/deliverables/post-deploy-report.md` *(pendiente)*

---

## 6.7 Rollback Plan (5 deliverables)

**Responsable:** DevOps Lead | **Aprueba:** Tech Lead

---

### 6.7.1 Rollback Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.7 Rollback Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + por release |

**Perfil de ejecución:** Requiere planificar reversión completa: código, migrations, config.  
En VTT: un agente puede generar el plan. Es altamente delegable.

**Qué es:** Plan de reversión: qué se revierte (código: previous image, migrations: down migration, config: previous env vars), en qué orden, y quién ejecuta.

**Para qué sirve:** Sin plan, un deploy fallido a las 3AM es caos. El plan responde todas las preguntas antes de que se necesiten.

**Inputs requeridos:**
- `6.2.4` Deploy Scripts — rollback script
- `4.2.10` Rollback Scripts — DB rollback

**Dependencias (predecessors):**
- `6.2.4` Deploy Scripts *(obligatorio)*
- `4.2.10` Rollback Scripts *(obligatorio)*

**Habilita (successors):**
- `6.7.2` Rollback Scripts
- `6.7.3` Rollback Tested

**Audiencia:**
- **DevOps Lead** — ejecutor
- **Tech Lead** — decision maker
- **On-call team** — backup

**Secciones esperadas:**
1. Rollback strategy
2. Step-by-step procedure
3. Previous version identifier
4. Data considerations (data loss?)
5. Time estimate
6. Communication plan
7. Verification post-rollback

**Criterio de completitud:**
- [ ] Procedure step-by-step
- [ ] Previous version identificada
- [ ] Data loss assessment
- [ ] Time estimate
- [ ] Communication plan

**Anti-patrones:**
- ❌ **Sin plan:** Caos bajo presión.
- ❌ **Plan que nadie leyó:** Documento perdido en Google Drive.

**Template:** `phases/06-deploy/deliverables/rollback-plan.md` *(pendiente)*

---

### 6.7.2 Rollback Scripts

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.7 Rollback Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Shell |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Por release |

**Perfil de ejecución:** Requiere scripts automatizados para rollback rápido.  
En VTT: un agente puede generar rollback scripts. Es altamente delegable.

**Qué es:** Scripts automatizados: rollback.sh revierte deployment (previous Docker image), revierte migration (si reversible), restaura config anterior. Un solo comando.

**Para qué sirve:** Bajo presión, un script de un comando es infinitamente más seguro que pasos manuales.

**Inputs requeridos:**
- `6.7.1` Rollback Plan — procedure
- `6.2.4` Deploy Scripts — base

**Dependencias (predecessors):**
- `6.7.1` Rollback Plan *(obligatorio)*

**Habilita (successors):**
- `6.7.3` Rollback Tested

**Audiencia:**
- **DevOps Lead** — ejecución
- **On-call team** — emergencia

**Secciones esperadas:**
1. rollback.sh (revert to previous version)
2. rollback-db.sh (revert migration)
3. Pre-rollback checks
4. Post-rollback health check
5. Usage instructions

**Criterio de completitud:**
- [ ] Script revierte con un comando
- [ ] Pre-rollback backup
- [ ] Post-rollback health check
- [ ] Error handling
- [ ] Documentado

**Anti-patrones:**
- ❌ **Rollback manual:** 10 pasos bajo presión — errores garantizados.

**Template:** `phases/06-deploy/deliverables/rollback-scripts.sh` *(pendiente)*

---

### 6.7.3 Rollback Tested

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.7 Rollback Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Log |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Pre-production deploy |

**Perfil de ejecución:** Requiere ejecutar rollback en staging para verificar.  
En VTT: N/A — ejecución real del script.

**Qué es:** Evidencia de que rollback fue probado en staging: deploy → rollback → verificar que versión anterior funciona. Log como evidencia.

**Para qué sirve:** Rollback no probado puede fallar cuando se necesita. Probarlo en staging asegura que funciona.

**Inputs requeridos:**
- `6.7.2` Rollback Scripts — script a probar
- `6.3.1` Staging Deploy — ambiente

**Dependencias (predecessors):**
- `6.7.2` Rollback Scripts *(obligatorio)*
- `6.3.1` Staging Deploy *(obligatorio)*

**Habilita (successors):**
- `6.5.1` Production Deploy — prerequisito

**Audiencia:**
- **DevOps Lead** — ejecución
- **Tech Lead** — validation

**Secciones esperadas:**
1. Test execution log
2. Pre-rollback state
3. Rollback execution (output)
4. Post-rollback verification
5. Data integrity check
6. Time taken

**Criterio de completitud:**
- [ ] Rollback ejecutado en staging
- [ ] Versión anterior funciona post-rollback
- [ ] Health check pasa
- [ ] No data loss (o documentado)
- [ ] Time measured

**Anti-patrones:**
- ❌ **Nunca probado:** Primera ejecución es en producción a las 3AM.

**Template:** `phases/06-deploy/deliverables/rollback-test-log.md` *(pendiente)*

---

### 6.7.4 Rollback Runbook

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.7 Rollback Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + actualizaciones |

**Perfil de ejecución:** Requiere guía step-by-step ejecutable bajo presión por cualquier on-call.  
En VTT: un agente puede generar el runbook. Es altamente delegable.

**Qué es:** Guía step-by-step para rollback en producción: pre-requisitos, pasos exactos (copy-paste), verificación, notificaciones, y troubleshooting si rollback falla. Para cualquier miembro del on-call, no solo DevOps.

**Para qué sirve:** A las 3AM, DevOps puede no estar disponible. El runbook permite que otro ejecute siguiendo instrucciones.

**Inputs requeridos:**
- `6.7.1` Rollback Plan
- `6.7.2` Rollback Scripts

**Dependencias (predecessors):**
- `6.7.1` Rollback Plan *(obligatorio)*
- `6.7.2` Rollback Scripts *(obligatorio)*

**Habilita (successors):**
- On-call team puede ejecutar rollback autónomamente

**Audiencia:**
- **On-call team** — ejecución bajo presión

**Secciones esperadas:**
1. Pre-requisitos (access, tools)
2. Step 1: Assess
3. Step 2: Notify
4. Step 3: Execute (copy-paste ready)
5. Step 4: Verify
6. Step 5: Communicate
7. If rollback fails: escalation
8. Post-rollback: post-mortem

**Criterio de completitud:**
- [ ] Steps copy-paste ready
- [ ] Escalation path
- [ ] Probado por alguien que no lo escribió

**Anti-patrones:**
- ❌ **"Use your judgment":** Bajo presión no es momento de judgment.
- ❌ **Solo DevOps puede ejecutar:** Bus factor 1.

**Template:** `phases/06-deploy/deliverables/rollback-runbook.md` *(pendiente)*

---

### 6.7.5 Decision Criteria

| Campo | Valor |
|-------|-------|
| **Fase** | 6-Deploy |
| **Subfase** | 6.7 Rollback Plan |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere definir criterios objetivos para decisión de rollback.  
En VTT: un agente puede generar criterios. Es altamente delegable.

**Qué es:** Criterios medibles para decidir rollback: "si error rate > 5% por 10+ min", "si 3+ usuarios reportan mismo critical bug", "si health check falla > 5 min", "si data corruption detectada". Define quién decide y time limit para decisión (max 15 min debatiendo → rollback by default).

**Para qué sirve:** Sin criterios, se debate durante el outage. Criterios pre-definidos eliminan el debate — si se cumple, se ejecuta.

**Inputs requeridos:**
- `3B.8.10` SLA Definition — error budget
- `6.6.2` Alerts Configured

**Dependencias (predecessors):**
- `3B.8.10` SLA Definition *(obligatorio)*

**Habilita (successors):**
- Decisión rápida durante incidents

**Audiencia:**
- **Tech Lead** — decision maker
- **DevOps Lead** — executor
- **On-call team** — awareness

**Secciones esperadas:**
1. Rollback triggers (tabla: condition, threshold, auto/manual)
2. Decision makers
3. Decision process
4. Forward-fix vs rollback guidelines
5. Time limit (max 15 min → rollback by default)
6. Post-rollback actions

**Criterio de completitud:**
- [ ] 3+ rollback triggers con thresholds
- [ ] Decision makers identificados
- [ ] Time limit definido
- [ ] Default = rollback si hay duda
- [ ] Conocido por on-call team

**Anti-patrones:**
- ❌ **Sin criterios:** Debatir durante outage.
- ❌ **Criterios vagos:** "Si está mal" — ¿qué es "mal"?
- ❌ **Default = no rollback:** Bias humano de "intentar arreglar".

**Template:** `phases/06-deploy/deliverables/decision-criteria.md` *(pendiente)*

---

## Tabla resumen — Fase 6 Deploy

| Subfase | Deliverables | Responsable | Delegable VTT |
|---------|-------------|-------------|---------------|
| 6.1 Infrastructure Setup | 8 | DevOps Lead | ✅ IaC generables |
| 6.2 CI/CD Configuration | 6 | DevOps Lead | ✅ Pipeline YAML delegable |
| 6.3 Staging Deploy | 4 | DevOps Lead | ✅ Automatizado |
| 6.4 Smoke Testing | 3 | QA Engineer | 🔶 Checklist delegable, ejecución manual |
| 6.5 Production Deploy | 6 | DevOps Lead | 🔶 Deploy automatizado, release notes delegables |
| 6.6 Post-Deploy Monitoring | 6 | SRE | ✅ Configs delegables |
| 6.7 Rollback Plan | 5 | DevOps Lead | ✅ Plan, scripts, runbook delegables |
