# 🚀 SETUP EN HETZNER - Compartiendo PostgreSQL y Redis

## 📍 TU SITUACIÓN ACTUAL
- ✅ IP: 77.42.88.106
- ✅ Usuario: root
- ✅ Docker ya instalado y funcionando
- ✅ PostgreSQL corriendo en puerto 5432
- ✅ Redis corriendo en puerto 6379
- ✅ Espacio disponible: 50GB de 75GB
- ⚠️ RAM: 4GB total (optimizar recursos)

---

## 1️⃣ CREAR BASE DE DATOS SEPARADA EN POSTGRESQL EXISTENTE

### Conectar a PostgreSQL

```bash
# Desde tu VM
docker exec -it mediapro-postgres psql -U postgres
```

### Crear base de datos y usuario para Prompt AI Studio

```sql
-- Crear base de datos
CREATE DATABASE prompt_ai;

-- Crear usuario específico (opcional pero recomendado)
CREATE USER prompt_ai_user WITH PASSWORD 'tu_password_seguro_aqui';

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON DATABASE prompt_ai TO prompt_ai_user;

-- Conectar a la nueva base de datos
\c prompt_ai

-- Habilitar extensión pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Verificar que se creó correctamente
\l

-- Salir
\q
```

---

## 2️⃣ CONFIGURAR REDIS CON PREFIJO

Redis ya está corriendo, solo necesitas usar un **prefijo** para las keys de tu proyecto.

Ejemplo:
- MediaPro usa keys como: `job:123`, `user:456`
- Prompt AI Studio usará: `pai:job:123`, `pai:user:456`

Esto se configura en tu código, no en Redis.

---

## 3️⃣ CONFIGURAR FIREWALL PARA TU IP LOCAL

```bash
# En tu VM Hetzner

# Ver reglas actuales
ufw status

# Permitir tu IP local acceder a PostgreSQL y Redis
# Primero, obtén tu IP local
```

**Desde tu Windows (PowerShell), obtén tu IP:**
```powershell
Invoke-RestMethod -Uri "https://api.ipify.org"
```

**Luego en la VM:**
```bash
# Reemplaza TU_IP_LOCAL con la IP que obtuviste
ufw allow from TU_IP_LOCAL to any port 5432 comment 'PostgreSQL desde Windows'
ufw allow from TU_IP_LOCAL to any port 6379 comment 'Redis desde Windows'

# Verificar
ufw status numbered
```

---

## 4️⃣ PROBAR CONEXIÓN DESDE TU WINDOWS

### Test de PostgreSQL

```powershell
# En PowerShell (Windows)
Test-NetConnection -ComputerName 77.42.88.106 -Port 5432
# Debe decir: TcpTestSucceeded : True
```

### Conectar con psql (si tienes cliente instalado)

```powershell
# Instalar psql si no lo tienes:
# https://www.postgresql.org/download/windows/

# Conectar a la nueva base de datos
psql -h 77.42.88.106 -p 5432 -U prompt_ai_user -d prompt_ai
# Password: tu_password_seguro_aqui

# Probar
\l   # Listar bases de datos
\dt  # Listar tablas (aún vacío)
\q   # Salir
```

### Test de Redis

```powershell
Test-NetConnection -ComputerName 77.42.88.106 -Port 6379
# Debe decir: TcpTestSucceeded : True
```

---

## 5️⃣ ACTUALIZAR .ENV EN TUS REPOS LOCALES

### 1. core-engine/.env

```env
NODE_ENV=development
PORT=3001
INTERNAL_API_KEY=genera-un-secret-aleatorio-largo

# Database - PostgreSQL en Hetzner (nueva base de datos)
DATABASE_URL=postgresql://prompt_ai_user:tu_password_seguro_aqui@77.42.88.106:5432/prompt_ai

# Redis en Hetzner (con prefijo en código)
REDIS_URL=redis://77.42.88.106:6379
REDIS_PREFIX=pai:

# AI APIs
ANTHROPIC_API_KEY=tu-api-key-de-anthropic
OPENAI_API_KEY=tu-api-key-de-openai

# Clerk
CLERK_SECRET_KEY=
CLERK_WEBHOOK_SECRET=

# Security
JWT_SECRET=genera-un-secret-aleatorio-largo
ENCRYPTION_KEY=genera-otro-secret-aleatorio
```

### 2. api-gateway/.env

```env
PORT=3000
NODE_ENV=development

# Core Engine (localhost porque corre en tu máquina)
CORE_ENGINE_URL=http://localhost:3001
CORE_ENGINE_API_KEY=el-mismo-INTERNAL_API_KEY-del-core-engine

# Clerk
CLERK_SECRET_KEY=
CLERK_PUBLISHABLE_KEY=

# Frontend
FRONTEND_URL=http://localhost:5173
```

### 3. frontend/.env

```env
VITE_CLERK_PUBLISHABLE_KEY=
VITE_API_URL=http://localhost:3000/api
VITE_ENV=development
```

### 4. database/.env

```env
DATABASE_URL=postgresql://prompt_ai_user:tu_password_seguro_aqui@77.42.88.106:5432/prompt_ai
```

---

## 6️⃣ APLICAR MIGRACIONES DE PRISMA

### Desde tu repo database en Windows

```powershell
cd C:\users\martin\documents\prompt-ai-studio\prompt-ai-database

# Generar cliente Prisma
npx prisma generate

# Aplicar migraciones (crear tablas en la nueva BD)
npx prisma migrate dev --name init

# Verificar tablas creadas
npx prisma studio
# Se abrirá en el navegador y podrás ver las tablas vacías
```

---

## 7️⃣ VERIFICAR SEPARACIÓN DE DATOS

### Verificar que MediaPro y Prompt AI están separados

```bash
# Conectar a PostgreSQL
docker exec -it mediapro-postgres psql -U postgres

# Listar bases de datos
\l

# Deberías ver:
#  mediapro     <- Base de datos de MediaPro
#  prompt_ai    <- Base de datos de Prompt AI Studio (nueva)
#  postgres     <- Base de datos por defecto

# Ver tablas de cada base de datos
\c mediapro
\dt  # Tablas de MediaPro

\c prompt_ai
\dt  # Tablas de Prompt AI Studio

\q
```

---

## 8️⃣ MONITOREO DE RECURSOS

### Ver uso actual de recursos

```bash
# En la VM

# Ver RAM usada
free -h

# Ver CPU y RAM por contenedor
docker stats

# Ver espacio en disco
df -h

# Ver tamaño de cada base de datos
docker exec -it mediapro-postgres psql -U postgres -c "SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) AS size FROM pg_database;"
```

### Limitar recursos si es necesario

Si ves que la RAM está al límite, puedes limitar recursos de los contenedores:

```bash
# Ver configuración actual de mediapro
cd ~/mediapro-backend/backend/infra
cat docker-compose.yml | grep -A 5 mem_limit
```

---

## 9️⃣ LEVANTAR SERVICIOS LOCALES EN WINDOWS

### Terminal 1: Core Engine
```powershell
cd C:\users\martin\documents\prompt-ai-studio\prompt-ai-core-engine
npm run dev
```

Debería conectarse a PostgreSQL en Hetzner y mostrar:
```
🔒 Core Engine: port 3001
✅ Database connected
```

### Terminal 2: API Gateway
```powershell
cd C:\users\martin\documents\prompt-ai-studio\prompt-ai-api-gateway
npm run dev
```

### Terminal 3: Frontend
```powershell
cd C:\users\martin\documents\prompt-ai-studio\prompt-ai-frontend
npm run dev
```

### Probar que todo funciona

```powershell
# Test Core Engine
curl http://localhost:3001/health

# Test API Gateway  
curl http://localhost:3000/health

# Test Frontend
# Abrir: http://localhost:5173
```

---

## 🔟 BACKUP DE LA NUEVA BASE DE DATOS

### Crear script de backup automático

```bash
# En la VM, crear script
cat > ~/backup-prompt-ai.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/root/backups/prompt-ai"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup de PostgreSQL
docker exec mediapro-postgres pg_dump -U prompt_ai_user prompt_ai > $BACKUP_DIR/prompt_ai_$DATE.sql

# Mantener solo últimos 7 días
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete

echo "Backup completado: prompt_ai_$DATE.sql"
EOF

# Dar permisos
chmod +x ~/backup-prompt-ai.sh

# Probar
./backup-prompt-ai.sh
```

### Programar backup diario (cron)

```bash
# Editar crontab
crontab -e

# Agregar esta línea (backup diario a las 3 AM)
0 3 * * * /root/backup-prompt-ai.sh >> /root/backup-prompt-ai.log 2>&1
```

---

## 1️⃣1️⃣ GENERAR SECRETS ALEATORIOS

### Desde PowerShell (Windows)

```powershell
# Generar INTERNAL_API_KEY
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})

# Generar JWT_SECRET
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})

# Generar ENCRYPTION_KEY
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

Copia cada resultado y pégalo en los archivos `.env` correspondientes.

---

## 🎯 CHECKLIST FINAL

Antes de continuar a Fase 1:

- [ ] Base de datos `prompt_ai` creada en PostgreSQL
- [ ] Extensión `vector` habilitada en `prompt_ai`
- [ ] Usuario `prompt_ai_user` creado con permisos
- [ ] Firewall permite acceso desde tu IP a puertos 5432 y 6379
- [ ] Test de conexión exitoso desde Windows (`Test-NetConnection`)
- [ ] Archivos `.env` actualizados en los 4 repos
- [ ] Secrets aleatorios generados y configurados
- [ ] Migraciones de Prisma aplicadas (tablas creadas)
- [ ] Core Engine conecta exitosamente a PostgreSQL en Hetzner
- [ ] API Gateway corriendo (`localhost:3000`)
- [ ] Frontend corriendo (`localhost:5173`)
- [ ] Verificado que bases de datos están separadas (mediapro vs prompt_ai)

---

## 🔧 COMANDOS ÚTILES

### Ver logs de PostgreSQL
```bash
docker logs mediapro-postgres -f --tail 100
```

### Reiniciar solo PostgreSQL si es necesario
```bash
docker restart mediapro-postgres
```

### Conectar a PostgreSQL desde la VM
```bash
docker exec -it mediapro-postgres psql -U postgres -d prompt_ai
```

### Ver conexiones activas a prompt_ai
```sql
SELECT * FROM pg_stat_activity WHERE datname = 'prompt_ai';
```

---

## ⚠️ NOTAS IMPORTANTES

**1. Separación de datos:**
- MediaPro usa la base de datos `mediapro`
- Prompt AI Studio usa la base de datos `prompt_ai`
- NO hay conflicto entre ellos

**2. Redis compartido:**
- Usa el prefijo `pai:` para todas las keys
- Ejemplo en código Node.js:
```javascript
const redis = require('redis');
const client = redis.createClient({
  url: process.env.REDIS_URL,
  prefix: 'pai:' // Todas las keys tendrán este prefijo
});
```

**3. Monitoreo:**
- Vigila el uso de RAM (máximo 4GB)
- Si llega al límite, considera actualizar la VM o usar servicios externos para PostgreSQL

---

**¿Todo listo? Confirma que completaste el checklist y pasamos a la Fase 1** 🚀
