# DICCIONARIO DE DELIVERABLES — FASE 3B.8: INFRASTRUCTURE PLAN

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 3B — Design Technical  
**Subfase:** 3B.8 — Infrastructure Plan  
**Total deliverables:** 11  
**Responsable de subfase:** DevOps Lead  
**Aprueba:** Solution Architect

---

## Contexto de la subfase

Infrastructure Plan define la plataforma sobre la que corre el sistema: servidores, redes, ambientes, escalado, backups, disaster recovery, costos, SLAs, y monitoreo. Es el "mundo físico" (o cloud) donde vive el código. Una buena infraestructura es invisible — todo funciona. Una mala infraestructura produce downtime, latencia, y facturas sorpresa de cloud.

**Prerequisitos de subfase:**
- Solution Architecture (3B.1) — contenedores a desplegar
- Technology Stack (3B.1.5) — servicios y herramientas
- Security Plan (3B.7) — controles de seguridad en infra

**Entrega de subfase:**
- Infraestructura diseñada, costeada, y lista para provisionar antes del primer deploy

---

### 3B.8.1 Infrastructure Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.8 Infrastructure Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | MD/PDF |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + actualizaciones por cambio de escala |

**Perfil de ejecución:** Requiere experiencia en cloud infrastructure (AWS, GCP, Azure), IaC (Terraform, Pulumi), y capacity planning.  
En VTT: un agente puede generar la estructura del plan y compilar secciones a partir de los deliverables 3B.8.2-3B.8.11. NO puede tomar decisiones de sizing ni costos sin conocer los precios actuales y la carga esperada. Necesita brief con: cloud provider, servicios elegidos, carga esperada, budget, y SLA requerido.

**Qué es:** Documento maestro de infraestructura que consolida: diagrama de infra, especificaciones de servidores, diseño de red, ambientes, escalado, backups, disaster recovery, costos, SLAs, y monitoreo. Es la referencia completa para provisionar y operar la infraestructura del proyecto.

**Para qué sirve:** Sin plan de infraestructura, el DevOps "improvisa" en cloud: crea servidores a ojo, elige instance types al azar, no planea escalado, y el primer pico de tráfico tumba todo. El plan asegura que la infra está diseñada para la carga esperada, costeada dentro del budget, y preparada para escalar.

**Inputs requeridos:**
- `3B.1.3` Container Diagram — qué desplegar
- `3B.1.5` Technology Stack — servicios y herramientas
- `3B.3.8` Backup Strategy — backup de BD
- `3B.7.1` Security Plan — controles de seguridad en infra
- NFRs de performance, availability, scalability
- Budget de infraestructura

**Dependencias (predecessors):**
- `3B.1.3` Container Diagram *(obligatorio)* — contenedores a desplegar
- `3B.1.5` Technology Stack *(obligatorio)* — servicios
- `3B.7.1` Security Plan *(obligatorio)* — controles de seguridad

**Habilita (successors):**
- `3B.8.2` a `3B.8.11` — secciones detalladas
- `4.1.1` Environment Setup — provisión de ambientes
- `6.3.1` Production Environment Setup — setup de producción

**Audiencia:**
- **DevOps Lead** — documento propio
- **Solution Architect** — validación de capacidad
- **Tech Lead** — implicaciones para desarrollo
- **Finance / Management** — costos de infraestructura
- **Security Engineer** — seguridad de red y acceso

**Secciones esperadas:**
1. Overview de infraestructura (cloud provider, región, approach: IaC)
2. Diagrama de infraestructura (3B.8.2)
3. Server specifications (3B.8.3)
4. Network design (3B.8.4)
5. Environment matrix (3B.8.5)
6. Scaling strategy (3B.8.6)
7. Backup strategy (3B.8.7)
8. Disaster recovery (3B.8.8)
9. Cost estimate (3B.8.9)
10. SLA definition (3B.8.10)
11. Monitoring strategy (3B.8.11)
12. IaC approach (Terraform, Pulumi, CloudFormation)

**Criterio de completitud:**
- [ ] Todas las secciones (3B.8.2-3B.8.11) cubiertas
- [ ] Cloud provider y región definidos
- [ ] IaC approach definido
- [ ] Budget alineado con cost estimate
- [ ] Aprobado por Solution Architect

**Anti-patrones:**
- ❌ **Infra por click:** Crear recursos manualmente en la consola de AWS — no reproducible, no versionable.
- ❌ **Sin plan de costos:** "Ya veremos cuánto cuesta" — facturas sorpresa al final del mes.
- ❌ **Over-provisioning inicial:** 8 servidores para un MVP con 100 usuarios — desperdicio de budget.
- ❌ **Under-provisioning sin escalado:** 1 servidor para 10K usuarios sin auto-scaling — downtime en el primer pico.

**Template:** `phases/03B-design-technical/deliverables/infrastructure-plan.md` *(pendiente)*

---

### 3B.8.2 Infrastructure Diagram

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.8 Infrastructure Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez + actualizaciones por cambio de infra |

**Perfil de ejecución:** Requiere conocimiento de servicios cloud y networking para representar la infraestructura visualmente.  
En VTT: un agente puede generar el diagrama de infraestructura en Mermaid o Draw.io a partir de la descripción del DevOps Lead. Es altamente delegable. Necesita brief con: cloud provider, servicios usados, VPC/network layout, y conexiones entre componentes.

**Qué es:** Diagrama visual de toda la infraestructura: VPC, subnets (public/private), load balancers, application servers, databases, caches, CDN, DNS, queues, storage, y sus conexiones. Muestra cómo se mapea el Container Diagram (3B.1.3) a servicios cloud específicos (EC2, RDS, ElastiCache, S3, CloudFront, etc.).

**Para qué sirve:** Traduce la arquitectura lógica a infraestructura física/cloud. El Container Diagram dice "API server" — el Infrastructure Diagram dice "2x t3.large en us-east-1 detrás de un ALB en subnet privada". Es la referencia para provisionar y troubleshoot.

**Inputs requeridos:**
- `3B.1.3` Container Diagram — contenedores a mapear
- `3B.8.3` Server Specifications — sizing de cada componente
- `3B.8.4` Network Design — VPC y subnets
- Cloud provider services catalog

**Dependencias (predecessors):**
- `3B.1.3` Container Diagram *(obligatorio)*
- `3B.8.3` Server Specifications *(recomendado)*
- `3B.8.4` Network Design *(recomendado)*

**Habilita (successors):**
- `4.1.1` Environment Setup — provisión basada en el diagrama
- `6.3.1` Production Environment Setup — referencia visual

**Audiencia:**
- **DevOps Lead** — referencia para provisión
- **Solution Architect** — validación del mapping
- **Security Engineer** — seguridad de red visible

**Secciones esperadas:**
1. Diagrama completo de infraestructura (VPC, subnets, servicios)
2. Leyenda (servicio cloud por icono/color)
3. Zonas de disponibilidad (AZ distribution)
4. Flujo de tráfico (usuario → DNS → CDN → LB → app → DB)
5. Network boundaries (public vs private subnets)
6. Conexiones a servicios externos

**Criterio de completitud:**
- [ ] Todos los contenedores del Container Diagram mapeados a servicios cloud
- [ ] VPC y subnets representados
- [ ] Load balancers y DNS incluidos
- [ ] Public vs private network boundaries claros
- [ ] Leyenda incluida
- [ ] AZs para alta disponibilidad indicados

**Anti-patrones:**
- ❌ **Diagrama genérico:** Usar un diagrama de AWS de otro proyecto sin adaptarlo — no refleja la infra real.
- ❌ **Sin network boundaries:** Todo en una flat network sin subnets — security risk.
- ❌ **BD en subnet pública:** Database accesible desde internet — vulnerabilidad crítica.

**Template:** `phases/03B-design-technical/deliverables/infrastructure-diagram.mmd` *(pendiente)*

---

### 3B.8.3 Server Specifications

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.8 Infrastructure Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + ajustes post-profiling |

**Perfil de ejecución:** Requiere conocimiento de instance types de cloud providers y capacity planning básico.  
En VTT: un agente puede generar la tabla de server specs a partir de los contenedores y la carga esperada. Es bastante delegable. Necesita brief con: contenedores, carga esperada (requests/sec, users concurrentes), y cloud provider.

**Qué es:** Tabla que define las especificaciones de cada servidor/servicio: instance type (t3.medium, db.r5.large), CPU, RAM, storage, OS, cantidad de instancias, y justificación del sizing. Incluye todos los componentes: app servers, database, cache, queue, workers, y bastion/jump server.

**Para qué sirve:** Evita provisionar a ojo ("pongo un t2.micro y vemos"). El sizing se basa en la carga esperada y se documenta para poder escalar racionalmente. También permite estimar costos con precisión.

**Inputs requeridos:**
- `3B.1.3` Container Diagram — componentes a dimensionar
- NFRs de performance — requests/sec, latencia esperada
- Carga estimada — usuarios concurrentes, storage
- Cloud provider pricing

**Dependencias (predecessors):**
- `3B.1.3` Container Diagram *(obligatorio)*
- `3B.9.1` Technical Estimates *(recomendado)* — carga estimada

**Habilita (successors):**
- `3B.8.2` Infrastructure Diagram — specs etiquetadas
- `3B.8.9` Cost Estimate — costos por servidor
- `4.1.1` Environment Setup — provisión con specs correctas

**Audiencia:**
- **DevOps Lead** — provisión
- **Solution Architect** — validación de capacidad
- **Finance** — costos

**Secciones esperadas:**
1. Tabla de servidores (componente, instance type, CPU, RAM, storage, OS, cantidad, justificación)
2. Managed services (RDS, ElastiCache, S3 — tier y config)
3. Sizing rationale (cómo se llegó a cada spec)
4. Scaling triggers (cuándo escalar cada componente)
5. Reserved vs on-demand (optimización de costos)

**Criterio de completitud:**
- [ ] Todos los componentes dimensionados
- [ ] Instance type específico para cada uno
- [ ] Justificación de sizing documentada
- [ ] Managed services configurados
- [ ] Scaling triggers definidos

**Anti-patrones:**
- ❌ **t2.micro para todo:** Under-sizing para ahorrar — performance issues desde día 1.
- ❌ **m5.4xlarge para un MVP:** Over-sizing porque "mejor que sobre" — budget quemado.
- ❌ **Sin justificación:** "Elegimos r5.large porque sí" — imposible de evaluar o ajustar racionalmente.

**Template:** `phases/03B-design-technical/deliverables/server-specifications.md` *(pendiente)*

---

### 3B.8.4 Network Design

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.8 Infrastructure Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Diagrama + Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de networking en cloud: VPCs, subnets, security groups, NACLs, NAT gateways, VPN, y peering.  
En VTT: un agente puede generar el diseño de red con CIDR blocks, security groups, y network ACLs. Es bastante delegable. Necesita brief con: cloud provider, número de ambientes, componentes públicos vs privados, y requisitos de VPN/peering.

**Qué es:** Diseño de la red del proyecto: VPC configuration, CIDR blocks, subnets (public/private por AZ), security groups, NACLs, NAT gateways, DNS configuration, VPN (si aplica), y peering (si aplica). Define qué puede hablar con qué y a través de qué puertos.

**Para qué sirve:** El network design es la primera línea de defensa: si la BD está en una subnet privada sin acceso desde internet, un atacante no puede conectarse directamente. Los security groups son firewalls que limitan el tráfico. Sin network design, todo está en la misma red sin aislamiento — un componente comprometido expone todo.

**Inputs requeridos:**
- `3B.8.2` Infrastructure Diagram — componentes a conectar
- `3B.7.1` Security Plan — requisitos de network security
- Cloud provider networking primitives

**Dependencias (predecessors):**
- `3B.8.2` Infrastructure Diagram *(obligatorio)*
- `3B.7.1` Security Plan *(recomendado)*

**Habilita (successors):**
- `4.1.1` Environment Setup — VPC y networking provisionados
- `6.3.1` Production Environment Setup — network hardening

**Audiencia:**
- **DevOps Lead** — implementación
- **Security Engineer** — validación de aislamiento
- **Solution Architect** — validación

**Secciones esperadas:**
1. VPC configuration (CIDR block, region, AZs)
2. Subnet design (public: ALB, bastion; private: app, DB, cache)
3. CIDR allocation table
4. Security groups (tabla: SG name, inbound rules, outbound rules)
5. NACLs (si aplica)
6. NAT gateway configuration
7. DNS configuration (Route53, CloudFlare)
8. VPN / peering (si aplica)
9. Bastion / jump server (acceso SSH seguro)

**Criterio de completitud:**
- [ ] VPC con CIDR definido
- [ ] Subnets public y private en al menos 2 AZs
- [ ] Security groups por componente
- [ ] BD y cache en subnets privadas
- [ ] NAT gateway para egress de subnets privadas
- [ ] Bastion server para acceso administrativo

**Anti-patrones:**
- ❌ **Todo en subnet pública:** BD, cache, y app todos accesibles desde internet — superficie de ataque máxima.
- ❌ **Security groups abiertos:** Inbound 0.0.0.0/0 en todos los puertos — sin firewall efectivo.
- ❌ **Sin NAT gateway:** Subnets privadas sin egress — los servers no pueden descargar updates ni llegar a APIs externas.
- ❌ **Single AZ:** Todo en una sola zona de disponibilidad — si esa AZ cae, todo cae.

**Template:** `phases/03B-design-technical/deliverables/network-design.md` *(pendiente)*

---

### 3B.8.5 Environment Matrix

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.8 Infrastructure Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere entendimiento de ambientes de desarrollo y deployment pipelines.  
En VTT: un agente puede generar la environment matrix completa. Es altamente delegable. Necesita brief con: ambientes requeridos, propósito de cada uno, sizing, y acceso.

**Qué es:** Tabla que define todos los ambientes del proyecto: development (local), dev (shared), staging/QA, pre-production, production. Para cada ambiente: propósito, sizing (igual a prod o reducido), datos (fake, sanitized, real), acceso (quién puede acceder), URL, y cómo se despliega.

**Para qué sirve:** Sin environment matrix, cada developer tiene una idea diferente de qué es "staging" y qué datos tiene. La matrix estandariza: staging es "producción chica con datos sanitizados, accesible por QA, deploy automático desde branch main".

**Inputs requeridos:**
- `3B.8.3` Server Specifications — sizing por ambiente
- `3B.3.7` Seed Data Plan — datos por ambiente
- Proceso de deploy (CI/CD pipeline)

**Dependencias (predecessors):**
- `3B.8.3` Server Specifications *(recomendado)*

**Habilita (successors):**
- `4.1.1` Environment Setup — creación de ambientes
- `4.1.4` CI/CD Pipeline — deploy targets
- `3B.7.8` Secrets Management — secrets por ambiente

**Audiencia:**
- **Todo el equipo** — saber qué ambiente usar para qué
- **DevOps Lead** — provisión y mantenimiento
- **QA Engineer** — saber dónde testear

**Secciones esperadas:**
1. Tabla de ambientes (nombre, propósito, sizing, datos, URL, deploy method, acceso)
2. Data strategy por ambiente (fake, sanitized, real)
3. Parity con producción (qué es igual, qué es diferente)
4. Refresh policy (cuándo se resetea cada ambiente)
5. Access control (quién puede acceder a qué ambiente)

**Criterio de completitud:**
- [ ] Al menos 3 ambientes definidos (dev, staging, prod)
- [ ] Propósito claro de cada ambiente
- [ ] Datos por ambiente definidos (nunca datos reales fuera de prod)
- [ ] URLs definidas
- [ ] Access control documentado

**Anti-patrones:**
- ❌ **Solo dev y prod:** Sin staging — los bugs se descubren en producción.
- ❌ **Datos de prod en staging:** Datos reales de usuarios en un ambiente menos protegido — data leak.
- ❌ **Staging muy diferente a prod:** Diferente OS, diferente DB version, diferente config — "funciona en staging" no garantiza nada.

**Template:** `phases/03B-design-technical/deliverables/environment-matrix.md` *(pendiente)*

---

### 3B.8.6 Scaling Strategy

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.8 Infrastructure Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez + ajustes post-producción |

**Perfil de ejecución:** Requiere experiencia en auto-scaling, horizontal vs vertical scaling, y capacity planning.  
En VTT: un agente puede documentar la estrategia de scaling. Es bastante delegable. Necesita brief con: componentes a escalar, métricas de scaling (CPU, memory, request count), y thresholds.

**Qué es:** Documento que define cómo escala cada componente del sistema: horizontal (más instancias) vs vertical (más recursos), auto-scaling policies (triggers, min/max instances, cooldown), database scaling (read replicas, connection pooling, sharding plan), y cache scaling.

**Para qué sirve:** El tráfico no es constante — hay picos (lanzamiento, campaña, Black Friday). Sin scaling strategy, el sistema o está sobre-provisionado (costoso) o se cae en picos. Auto-scaling balancea costo y disponibilidad automáticamente.

**Inputs requeridos:**
- `3B.8.3` Server Specifications — baseline sizing
- NFRs de performance y availability
- Proyección de tráfico (ramp-up, picos, estacionalidad)

**Dependencias (predecessors):**
- `3B.8.3` Server Specifications *(obligatorio)*
- `3B.1.3` Container Diagram *(obligatorio)*

**Habilita (successors):**
- `4.1.1` Environment Setup — auto-scaling configurado
- `7.1.1` Monitoring Setup — scaling metrics monitoreadas
- `3B.8.9` Cost Estimate — costos de scaling incluidos

**Audiencia:**
- **DevOps Lead** — implementación
- **Solution Architect** — validación de capacidad
- **Finance** — costos variables de scaling

**Secciones esperadas:**
1. Scaling type por componente (horizontal, vertical, managed auto-scale)
2. Auto-scaling policies (tabla: componente, metric, threshold, min, max, cooldown)
3. Database scaling (read replicas, connection pooling, sharding triggers)
4. Cache scaling (cluster mode, eviction policy)
5. CDN y static assets (edge caching, invalidation)
6. Queue/worker scaling (queue depth triggers)
7. Projected capacity (tabla: usuarios concurrentes → resources necesarios)
8. Load testing plan (verificar que el scaling funciona)

**Criterio de completitud:**
- [ ] Cada componente stateless tiene auto-scaling configurado
- [ ] Métricas y thresholds definidos
- [ ] Database scaling strategy definida
- [ ] Projected capacity para al menos 3 niveles de tráfico
- [ ] Load testing planificado

**Anti-patrones:**
- ❌ **Sin auto-scaling:** Scaling manual a las 3AM cuando el sistema se cae — inaceptable.
- ❌ **Scaling solo de app servers:** La app escala pero la BD no — cuello de botella se mueve.
- ❌ **Thresholds agresivos:** Scale up at 30% CPU — instancias innecesarias, costo inflado.
- ❌ **Sin cooldown:** Scale up y scale down en loop — flapping que desperdicia recursos.

**Template:** `phases/03B-design-technical/deliverables/scaling-strategy.md` *(pendiente)*

---

### 3B.8.7 Backup Strategy

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.8 Infrastructure Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere experiencia con backup/restore en la infraestructura cloud elegida.  
En VTT: un agente puede documentar la estrategia de backup de infraestructura. Es bastante delegable. Necesita brief con: componentes a respaldar, herramientas de backup del cloud provider, y RPO/RTO.

**Qué es:** Extensión de la Backup Strategy de BD (3B.3.8) para cubrir toda la infraestructura: file storage (S3 versioning, cross-region replication), configuration backups (IaC state files, secrets), application artifacts (Docker images, deployment packages), y logs. Complementa el backup de BD con todo lo demás que necesita backup.

**Para qué sirve:** La BD no es lo único que necesita backup. Si se pierde el Terraform state, no se puede gestionar la infra. Si se pierden los Docker images, no se puede hacer rollback. Si se pierden los logs, no se puede investigar un incident. Esta estrategia cubre todo lo que no cubre 3B.3.8.

**Inputs requeridos:**
- `3B.3.8` Backup Strategy — backup de BD (ya cubierto)
- `3B.8.1` Infrastructure Plan — componentes a respaldar
- IaC state files location

**Dependencias (predecessors):**
- `3B.3.8` Backup Strategy *(obligatorio)* — referencia cruzada
- `3B.8.1` Infrastructure Plan *(obligatorio)*

**Habilita (successors):**
- `3B.8.8` Disaster Recovery Plan — backups como mecanismo de recovery
- `7.2.1` Backup Verification — testing de todos los backups

**Audiencia:**
- **DevOps Lead** — implementación
- **Security Engineer** — backups encriptados

**Secciones esperadas:**
1. Scope (qué se respalda además de la BD — referencia a 3B.3.8 para BD)
2. File storage backups (versioning, cross-region replication)
3. IaC state backups (Terraform state en S3 con versioning y locking)
4. Container images (registry, retention)
5. Configuration backups (secrets, env configs)
6. Log archival (long-term storage)
7. Tabla resumen (componente, método, frecuencia, retención, encriptación)

**Criterio de completitud:**
- [ ] File storage backup configurado
- [ ] IaC state con backup y locking
- [ ] Container images en registry con retention policy
- [ ] Logs archivados para long-term
- [ ] Todo encriptado
- [ ] Complementario a 3B.3.8 (sin duplicar BD)

**Anti-patrones:**
- ❌ **Solo backup de BD:** Perder el Terraform state = no poder gestionar la infra.
- ❌ **IaC state local:** `terraform.tfstate` en el laptop del DevOps — si pierde el laptop, pierde el control de la infra.
- ❌ **Sin retention de images:** Borrar Docker images antiguos imposibilita rollbacks.

**Template:** `phases/03B-design-technical/deliverables/infra-backup-strategy.md` *(pendiente)*

---

### 3B.8.8 Disaster Recovery Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.8 Infrastructure Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + simulacros anuales |

**Perfil de ejecución:** Requiere experiencia en disaster recovery: RPO/RTO, multi-region, failover, y recovery procedures.  
En VTT: un agente puede generar el DRP basándose en el tier de DR elegido (backup/restore, pilot light, warm standby, multi-site). Es bastante delegable. Necesita brief con: RPO/RTO aprobados, tier de DR, y cloud provider capabilities.

**Qué es:** Plan que define cómo se recupera el sistema ante un desastre mayor: pérdida de una región cloud, corrupción masiva de datos, o ataque destructivo. Define: RPO/RTO, tier de DR (backup/restore, pilot light, warm standby, multi-site active-active), failover procedures, recovery runbooks, y frecuencia de simulacros.

**Para qué sirve:** Desastres pasan: AWS us-east-1 se ha caído, data centers se incendian, ransomware encripta todo. El DRP asegura que el sistema puede recuperarse en un tiempo aceptable (RTO) con una pérdida de datos aceptable (RPO). Sin DRP, un desastre = pérdida total.

**Inputs requeridos:**
- `3B.3.8` Backup Strategy — backups como mecanismo de recovery
- `3B.8.7` Backup Strategy (infra) — backups de infra
- RPO/RTO aprobados por negocio
- Cloud provider DR capabilities

**Dependencias (predecessors):**
- `3B.3.8` Backup Strategy *(obligatorio)*
- `3B.8.7` Backup Strategy (infra) *(obligatorio)*
- `3B.8.1` Infrastructure Plan *(obligatorio)*

**Habilita (successors):**
- `7.2.1` Backup Verification — DR testing
- Simulacros de DR — basados en el plan

**Audiencia:**
- **DevOps Lead** — implementación y testing
- **Solution Architect** — validación
- **Management** — RPO/RTO son decisiones de negocio
- **Compliance** — evidencia de business continuity

**Secciones esperadas:**
1. RPO y RTO definidos y aprobados
2. DR tier elegido (backup/restore, pilot light, warm standby, multi-site)
3. Failover procedure step-by-step
4. Recovery runbook (cómo restaurar cada componente)
5. Data recovery procedure (restore de BD, files, configs)
6. DNS failover (Route53 health checks, failover records)
7. Communication plan durante DR (quién notificar, status page)
8. Simulacros (frecuencia, scope, success criteria)
9. Costo del DR approach elegido

**Criterio de completitud:**
- [ ] RPO/RTO definidos con aprobación de negocio
- [ ] DR tier elegido con justificación de costo
- [ ] Failover procedure documentado step-by-step
- [ ] Recovery runbook probado
- [ ] Simulacros programados
- [ ] Costo de DR estimado

**Anti-patrones:**
- ❌ **"El cloud nunca se cae":** AWS regions se han caído múltiples veces — no tener DR es jugar a la ruleta.
- ❌ **DR plan nunca probado:** El plan dice 1h de RTO pero nunca se probó — podría ser 24h en realidad.
- ❌ **Multi-site active-active para un MVP:** Costo de 10x para disponibilidad que no se necesita — backup/restore es suficiente para muchos proyectos.
- ❌ **Runbooks desactualizados:** Procedure de recovery que referencia servicios que ya no existen.

**Template:** `phases/03B-design-technical/deliverables/disaster-recovery-plan.md` *(pendiente)*

---

### 3B.8.9 Cost Estimate

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.8 Infrastructure Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez + revisión mensual post-producción |

**Perfil de ejecución:** Requiere conocimiento del pricing model del cloud provider y herramientas de cost estimation (AWS Calculator, GCP Calculator).  
En VTT: un agente puede generar la estimación de costos a partir de las server specifications y los servicios elegidos. Necesita brief con: server specs, servicios cloud, región, y pricing tier (on-demand, reserved, spot). Necesita acceso a calculadoras de pricing actualizadas.

**Qué es:** Estimación detallada del costo mensual de infraestructura: compute (servers, functions), storage (DB, files, backups), networking (data transfer, load balancers, CDN), managed services (cache, queue, monitoring), y otros (domains, certificates, third-party SaaS). Desglosa por ambiente (dev cuesta diferente a prod).

**Para qué sirve:** Evita sorpresas de facturación. Permite comparar approaches (serverless vs containers, reserved vs on-demand) con números reales. Permite al management aprobar el budget de infra antes de provisionar. También sirve como baseline para detectar cost anomalies en producción.

**Inputs requeridos:**
- `3B.8.3` Server Specifications — sizing de cada componente
- `3B.8.5` Environment Matrix — ambientes a costear
- Cloud provider pricing (AWS Calculator, GCP Calculator)
- Third-party SaaS costs (monitoring, email, etc.)

**Dependencias (predecessors):**
- `3B.8.3` Server Specifications *(obligatorio)*
- `3B.8.5` Environment Matrix *(obligatorio)*

**Habilita (successors):**
- Budget approval — management aprueba el gasto
- `7.4.1` Cost Monitoring — baseline para alertas de costo

**Audiencia:**
- **Finance / Management** — aprobación de budget
- **DevOps Lead** — referencia de costos
- **Solution Architect** — validación de cost-efficiency

**Secciones esperadas:**
1. Resumen ejecutivo (costo mensual total, costo anual)
2. Desglose por categoría (compute, storage, networking, managed services, SaaS)
3. Desglose por ambiente (dev, staging, prod)
4. Desglose por componente (API server, DB, cache, CDN, etc.)
5. Optimizaciones aplicadas (reserved instances, spot, savings plans)
6. Costos variables (data transfer, API calls — estimación por volumen)
7. Costos de scaling (costo adicional por tier de tráfico)
8. Comparativa de approaches (si se evaluaron alternativas)
9. Cost optimization recommendations

**Criterio de completitud:**
- [ ] Todos los componentes de infra costeados
- [ ] Costos por ambiente desglosados
- [ ] Optimizaciones de costo documentadas
- [ ] Costos variables estimados
- [ ] Total mensual y anual calculado
- [ ] Aprobado por management/finance

**Anti-patrones:**
- ❌ **Estimación sin data transfer:** Olvidar los costos de networking — pueden ser significativos.
- ❌ **Solo costos de producción:** No costear dev y staging — esos ambientes también cuestan.
- ❌ **Sin optimización:** Todo on-demand cuando reserved instances ahorran 30-50%.
- ❌ **Estimación de una sola vez:** No revisar costos reales vs estimados — drift silencioso.

**Template:** `phases/03B-design-technical/deliverables/cost-estimate.md` *(pendiente)*

---

### 3B.8.10 SLA Definition

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.8 Infrastructure Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead / Solution Architect |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere entendimiento de SLAs, SLOs, SLIs, y cómo definir targets de disponibilidad y performance realistas.  
En VTT: un agente puede generar las definiciones de SLA/SLO/SLI. Es bastante delegable. Necesita brief con: targets de disponibilidad (99.9%, 99.99%), latencia aceptable, y error budget.

**Qué es:** Definición de los Service Level Agreements/Objectives/Indicators del sistema: disponibilidad target (99.9% = 8.7h downtime/año), latencia target (p95 < 200ms), error rate target (<0.1%), y throughput target. Define SLIs (qué se mide), SLOs (targets internos), y SLAs (compromisos con usuarios/clientes).

**Para qué sirve:** Sin SLAs, no hay criterio objetivo para juzgar si el sistema "funciona bien". 99.9% de uptime suena alto pero permite 8.7 horas de downtime al año — ¿es aceptable para el negocio? Las SLAs alinean expectativas entre negocio y técnica, y definen el error budget (cuánto downtime o degradación se puede tolerar antes de frenar features nuevas para priorizar estabilidad).

**Inputs requeridos:**
- NFRs de availability y performance
- Expectativas del negocio
- SLAs de providers (cloud, third-party) — el SLA del sistema no puede ser mayor que el de sus providers
- `3B.8.6` Scaling Strategy — capacidad de recovery

**Dependencias (predecessors):**
- `3B.8.1` Infrastructure Plan *(obligatorio)*
- NFRs de negocio

**Habilita (successors):**
- `3B.8.11` Monitoring Strategy — SLIs monitoreados
- `7.1.1` Monitoring Setup — dashboards de SLOs
- `7.3.1` Incident Management — escalation basado en SLA breach

**Audiencia:**
- **Management** — compromisos de disponibilidad
- **DevOps Lead** — targets a mantener
- **Solution Architect** — validación de feasibility
- **Clientes** — SLAs contractuales (si aplica)

**Secciones esperadas:**
1. SLIs definidos (availability, latency p50/p95/p99, error rate, throughput)
2. SLOs por SLI (target: 99.9% availability, p95 latency < 200ms)
3. SLAs (compromisos formales con clientes, si aplica)
4. Error budget (cuánto margen hay para experimentar/fallar)
5. SLA composition (SLA del sistema vs SLA de providers)
6. Measurement methodology (cómo se mide cada SLI)
7. Reporting frequency (dashboards, monthly reports)
8. Breach response (qué pasa cuando se rompe un SLO)

**Criterio de completitud:**
- [ ] SLIs definidos para availability, latency, error rate
- [ ] SLOs con targets numéricos
- [ ] Error budget calculado
- [ ] Measurement methodology definida
- [ ] Breach response documentado
- [ ] SLAs no exceden los de los providers

**Anti-patrones:**
- ❌ **99.999% sin justificación:** Five nines requiere inversión masiva — ¿realmente lo necesita un MVP?
- ❌ **SLA sin medición:** Prometer 99.9% uptime sin herramienta de medición — no se puede cumplir lo que no se mide.
- ❌ **SLA mayor que el provider:** SLA de 99.99% cuando el cloud provider da 99.95% — matemáticamente imposible.
- ❌ **Sin error budget:** Zero tolerance to failure — frena la innovación y causa burnout.

**Template:** `phases/03B-design-technical/deliverables/sla-definition.md` *(pendiente)*

---

### 3B.8.11 Monitoring Strategy

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.8 Infrastructure Plan |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + ajustes continuos |

**Perfil de ejecución:** Requiere experiencia en observability: metrics, logs, traces (three pillars), y herramientas (Datadog, New Relic, Grafana, Prometheus, CloudWatch).  
En VTT: un agente puede generar la estrategia de monitoring con métricas clave, dashboards propuestos, y alerting rules. Es bastante delegable. Necesita brief con: herramientas elegidas, métricas clave, thresholds de alerta, y escalation policy.

**Qué es:** Estrategia que define qué se monitorea, cómo, y quién responde a las alertas. Cubre los tres pilares de observability: metrics (CPU, memory, request rate, error rate, latency), logs (structured, centralized, searchable), y traces (distributed tracing para debuggear latencia). Define dashboards, alertas, escalation, y on-call rotation.

**Para qué sirve:** Sin monitoring, los problemas se descubren cuando los usuarios se quejan. Con monitoring, el equipo detecta problemas antes que los usuarios: alta latencia, error rate creciente, disco lleno, memory leak. Las alertas proactivas reducen el MTTR (Mean Time to Recovery) y previenen outages.

**Inputs requeridos:**
- `3B.8.10` SLA Definition — SLIs a monitorear
- `3B.7.10` Security Logging — security events a monitorear
- `3B.1.5` Technology Stack — herramientas de monitoring
- `3B.8.3` Server Specifications — recursos a monitorear

**Dependencias (predecessors):**
- `3B.8.10` SLA Definition *(obligatorio)* — qué medir
- `3B.1.5` Technology Stack *(obligatorio)* — herramientas

**Habilita (successors):**
- `7.1.1` Monitoring Setup — implementación
- `7.3.1` Incident Management — alertas disparan incidents
- `7.1.2` Dashboards — visualización de métricas

**Audiencia:**
- **DevOps Lead** — implementación y mantenimiento
- **Todo el equipo técnico** — dashboards
- **Management** — health del sistema

**Secciones esperadas:**
1. Herramientas elegidas (metrics, logs, traces, APM)
2. Metrics (tabla: métrica, fuente, threshold warning, threshold critical)
3. Infrastructure metrics (CPU, memory, disk, network)
4. Application metrics (request rate, error rate, latency p50/p95/p99)
5. Business metrics (signups, orders, conversion rate)
6. Logs (formato, centralización, retención, búsqueda)
7. Distributed tracing (herramienta, sampling rate)
8. Dashboards propuestos (overview, per-service, per-endpoint)
9. Alerting rules (tabla: alerta, condition, severity, notification channel)
10. On-call rotation (quién responde, horarios, escalation)
11. Runbooks por alerta (qué hacer cuando dispara cada alerta)

**Criterio de completitud:**
- [ ] Los tres pilares cubiertos (metrics, logs, traces)
- [ ] SLIs del SLA Definition monitoreados
- [ ] Alertas definidas con thresholds
- [ ] Dashboards propuestos
- [ ] On-call rotation definida
- [ ] Runbooks para alertas críticas
- [ ] Herramientas elegidas y justificadas

**Anti-patrones:**
- ❌ **Solo métricas de infra:** Monitorear CPU pero no error rate — no detecta bugs que no consumen CPU.
- ❌ **Alertas sin runbooks:** La alerta dispara pero nadie sabe qué hacer — panic debugging a las 3AM.
- ❌ **Demasiadas alertas:** 50 alertas donde 45 son noise — alert fatigue, las alertas reales se ignoran.
- ❌ **Sin business metrics:** Monitorear infra pero no signups ni orders — el sistema puede estar "up" pero el negocio "down".
- ❌ **Logs no centralizados:** Logs en cada servidor sin aggregación — imposible correlacionar events.

**Template:** `phases/03B-design-technical/deliverables/monitoring-strategy.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3B.8 Infrastructure Plan

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3B.8.1 Infrastructure Plan | DevOps Lead | DevOps Lead | 🔶 Parcial — puede compilar plan, sizing requiere expertise |
| 3B.8.2 Infrastructure Diagram | DevOps Lead | DevOps Lead | ✅ — puede generar diagrama en Mermaid desde descripción |
| 3B.8.3 Server Specifications | DevOps Lead | DevOps Lead | 🔶 Parcial — puede generar tabla, pero sizing requiere capacity planning |
| 3B.8.4 Network Design | DevOps Lead | DevOps Lead | ✅ — puede generar diseño de red basado en best practices del cloud |
| 3B.8.5 Environment Matrix | DevOps Lead | DevOps Lead | ✅ — altamente delegable |
| 3B.8.6 Scaling Strategy | DevOps Lead | DevOps Lead | 🔶 Parcial — puede documentar strategy, thresholds requieren profiling |
| 3B.8.7 Backup Strategy | DevOps Lead | DevOps Lead | ✅ — puede documentar strategy de infra backups |
| 3B.8.8 Disaster Recovery Plan | DevOps Lead | DevOps Lead | 🔶 Parcial — puede generar DRP, pero RPO/RTO y tier son decisiones de negocio |
| 3B.8.9 Cost Estimate | DevOps Lead | DevOps Lead | 🔶 Parcial — puede estimar con calculadoras pero necesita pricing actualizado |
| 3B.8.10 SLA Definition | DevOps Lead | DevOps Lead / Solution Architect | 🔶 Parcial — puede definir SLIs/SLOs, targets son decisiones de negocio |
| 3B.8.11 Monitoring Strategy | DevOps Lead | DevOps Lead | ✅ — puede generar estrategia completa con métricas y alertas |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03B_09_TECHNICAL_ESTIMATES.md` — 9 deliverables (3B.9.1 a 3B.9.9)
