-- =====================================================
-- SEED: Catálogos VTT Modelo Dinámico V4
-- Versión: 2.0 (actualizado 2026-05-06)
-- Ejecutar en orden
-- =====================================================

-- =====================================================
-- 1. CRITERIA TYPE CATALOG
-- Tipos de criterios de aceptación
-- =====================================================

INSERT INTO criteria_type_catalog (code, name, description, icon_url, icon_type, is_active, "order") VALUES
('functional', 'Funcional', 'Comportamiento esperado del sistema', NULL, 'lucide:check-circle', true, 1),
('technical', 'Técnico', 'Requisito de implementación técnica', NULL, 'lucide:code', true, 2),
('ux', 'UX', 'Experiencia de usuario', NULL, 'lucide:user', true, 3),
('security', 'Seguridad', 'Requisitos de seguridad', NULL, 'lucide:shield', true, 4),
('performance', 'Rendimiento', 'Requisitos de performance', NULL, 'lucide:zap', true, 5),
('accessibility', 'Accesibilidad', 'Requisitos de accesibilidad', NULL, 'lucide:eye', true, 6),
('integration', 'Integración', 'Requisitos de integración con otros sistemas', NULL, 'lucide:plug', true, 7),
('dod', 'Definition of Done', 'Criterio de completitud de tarea', NULL, 'lucide:check-square', true, 8),
('dor', 'Definition of Ready', 'Precondición para iniciar tarea', NULL, 'lucide:play-circle', true, 9)
ON CONFLICT (code) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  icon_type = EXCLUDED.icon_type,
  is_active = EXCLUDED.is_active,
  "order" = EXCLUDED."order";

-- =====================================================
-- 2. TASK TYPE CATALOG (NUEVO)
-- Tipos de tarea para herencia de DoD
-- =====================================================

CREATE TABLE IF NOT EXISTS task_type_catalog (
  code VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  parent_category VARCHAR(50),
  project_type_code VARCHAR(50),
  dod_template_group VARCHAR(50),
  sort_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO task_type_catalog (code, name, description, parent_category, project_type_code, dod_template_group, sort_order, is_active) VALUES
('backend', 'Backend Development', 'Endpoints, servicios, lógica de negocio', 'development', 'software', 'DOD-BE', 1, true),
('frontend', 'Frontend Development', 'Componentes UI, vistas, interacción', 'development', 'software', 'DOD-FE', 2, true),
('database', 'Database', 'Schema, migrations, seeds, índices', 'development', 'software', 'DOD-BE', 3, true),
('documentation', 'Documentation / Analysis', 'Documentos SDLC, análisis, specs', 'documentation', 'software', 'DOD-DOC', 4, true),
('testing', 'QA Testing', 'Tests, validación, certificación', 'testing', 'software', 'DOD-QA', 5, true),
('devops', 'Infrastructure / DevOps', 'Docker, CI/CD, monitoreo, deployment', 'development', 'software', 'DOD-BE', 6, true),
('design', 'Design', 'Wireframes, design system, specs UX', 'design', 'software', 'DOD-DL', 7, true),
('research', 'Research', 'Investigación, spikes, PoC', 'analysis', 'software', NULL, 8, true),
('meeting', 'Meeting', 'Reuniones, ceremonies', 'coordination', 'software', NULL, 9, true)
ON CONFLICT (code) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  parent_category = EXCLUDED.parent_category,
  project_type_code = EXCLUDED.project_type_code,
  dod_template_group = EXCLUDED.dod_template_group,
  sort_order = EXCLUDED.sort_order,
  is_active = EXCLUDED.is_active;

-- =====================================================
-- 3. DEVLOG CATEGORY CATALOG
-- Categorías para entradas de devlog
-- =====================================================

INSERT INTO devlog_category_catalog (code, name, description, icon_url, icon_type, severity_levels, is_active, "order") VALUES
('issue', 'Issue', 'Observación o inconsistencia detectada (NO bugs)', NULL, 'lucide:alert-circle', ARRAY['critical','high','medium','low'], true, 1),
('tech_debt', 'Tech Debt', 'Deuda técnica identificada para resolver después', NULL, 'lucide:clock', ARRAY['critical','high','medium','low'], true, 2),
('decision', 'Decision', 'Decisión técnica o de proceso tomada', NULL, 'lucide:git-branch', ARRAY[]::text[], true, 3),
('blocker', 'Blocker', 'Algo que bloquea el avance del trabajo', NULL, 'lucide:octagon', ARRAY['critical','high','medium','low'], true, 4),
('risk', 'Risk', 'Riesgo identificado que requiere atención', NULL, 'lucide:alert-triangle', ARRAY['critical','high','medium','low'], true, 5),
('testing_note', 'Testing Note', 'Resultado o nota de testing/QA', NULL, 'lucide:clipboard-check', ARRAY['critical','high','medium','low'], true, 6),
('observation', 'Observation', 'Observación general durante ejecución', NULL, 'lucide:eye', ARRAY[]::text[], true, 7),
('question', 'Question', 'Pregunta pendiente de resolver', NULL, 'lucide:help-circle', ARRAY['high','medium','low'], true, 8)
ON CONFLICT (code) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  icon_type = EXCLUDED.icon_type,
  severity_levels = EXCLUDED.severity_levels,
  is_active = EXCLUDED.is_active,
  "order" = EXCLUDED."order";

-- =====================================================
-- 4. LINK TYPE CATALOG
-- Tipos de relaciones entre tareas/items
-- =====================================================

INSERT INTO link_type_catalog (code, name, description, icon_url, icon_type, is_active, "order") VALUES
('implements', 'Implements', 'Tarea implementa el item/requerimiento', NULL, 'lucide:check', true, 1),
('depends_on', 'Depends On', 'Tarea depende de otra para comenzar', NULL, 'lucide:arrow-right', true, 2),
('blocks', 'Blocks', 'Tarea bloquea a otra', NULL, 'lucide:octagon', true, 3),
('related_to', 'Related To', 'Tareas relacionadas sin dependencia directa', NULL, 'lucide:link', true, 4),
('parent_of', 'Parent Of', 'Tarea es padre de otra (subtareas)', NULL, 'lucide:folder', true, 5),
('child_of', 'Child Of', 'Tarea es hija de otra', NULL, 'lucide:file', true, 6),
('duplicates', 'Duplicates', 'Tarea duplica a otra', NULL, 'lucide:copy', true, 7),
('supersedes', 'Supersedes', 'Tarea reemplaza a otra', NULL, 'lucide:replace', true, 8),
('tests', 'Tests', 'Test case verifica este item (US, RF)', NULL, 'lucide:test-tube', true, 9),
('traces_to', 'Traces To', 'Item traza a otro (RF→US, US→AC)', NULL, 'lucide:git-commit', true, 10)
ON CONFLICT (code) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  icon_type = EXCLUDED.icon_type,
  is_active = EXCLUDED.is_active,
  "order" = EXCLUDED."order";

-- =====================================================
-- 5. LIVING DOC SOURCE CATALOG
-- Fuentes para documentos que se auto-generan
-- =====================================================

INSERT INTO living_doc_source_catalog (code, name, description, icon_url, icon_type, generation_type, parser_service, source_table, source_file_path, is_active, "order") VALUES
('prisma_schema', 'Prisma Schema', 'Genera documentación de modelo de datos desde schema.prisma', NULL, 'lucide:database', 'file', 'PrismaParserService', NULL, 'prisma/schema.prisma', true, 1),
('swagger_openapi', 'Swagger/OpenAPI', 'Genera documentación de API desde openapi.json o swagger.yaml', NULL, 'lucide:book-open', 'file', 'SwaggerParserService', NULL, 'swagger/openapi.json', true, 2),
('typescript_types', 'TypeScript Types', 'Genera documentación desde archivos .d.ts', NULL, 'lucide:file-type', 'file', 'TypeScriptParserService', NULL, 'src/types/index.d.ts', true, 3),
('env_template', 'Environment Template', 'Genera documentación de variables de entorno desde .env.example', NULL, 'lucide:settings', 'file', 'EnvParserService', NULL, '.env.example', true, 4),
('package_json', 'Package.json', 'Genera documentación de dependencias desde package.json', NULL, 'lucide:package', 'file', 'PackageJsonParserService', NULL, 'package.json', true, 5),
('db_query', 'Database Query', 'Genera documentación desde query a base de datos', NULL, 'lucide:database', 'query', 'DatabaseQueryService', NULL, NULL, true, 6)
ON CONFLICT (code) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  icon_type = EXCLUDED.icon_type,
  generation_type = EXCLUDED.generation_type,
  parser_service = EXCLUDED.parser_service,
  source_table = EXCLUDED.source_table,
  source_file_path = EXCLUDED.source_file_path,
  is_active = EXCLUDED.is_active,
  "order" = EXCLUDED."order";

-- =====================================================
-- 6. TRACKABLE TYPE CATALOG
-- Tipos de items rastreables
-- =====================================================

CREATE TABLE IF NOT EXISTS trackable_type_catalog (
  code VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  icon_type VARCHAR(100),
  is_active BOOLEAN DEFAULT true,
  sort_order INT DEFAULT 0
);

INSERT INTO trackable_type_catalog (code, name, description, icon_type, is_active, sort_order) VALUES
('rf', 'Requerimiento Funcional', 'Comportamiento esperado del sistema', 'lucide:check-circle', true, 1),
('rnf', 'Requerimiento No Funcional', 'Requisitos de calidad (performance, seguridad)', 'lucide:shield', true, 2),
('adr', 'Architecture Decision Record', 'Decisión arquitectónica documentada', 'lucide:git-branch', true, 3),
('kpi', 'Key Performance Indicator', 'Métrica de éxito', 'lucide:bar-chart', true, 4),
('risk', 'Riesgo', 'Riesgo identificado', 'lucide:alert-triangle', true, 5),
('constraint', 'Restricción', 'Limitación del proyecto', 'lucide:lock', true, 6),
('assumption', 'Supuesto', 'Supuesto asumido', 'lucide:help-circle', true, 7),
('dependency', 'Dependencia Externa', 'Dependencia de terceros', 'lucide:external-link', true, 8),
('bug', 'Bug', 'Defecto encontrado', 'lucide:bug', true, 9)
ON CONFLICT (code) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  icon_type = EXCLUDED.icon_type,
  is_active = EXCLUDED.is_active,
  sort_order = EXCLUDED.sort_order;

-- =====================================================
-- 7. VERIFICACIÓN
-- =====================================================

DO $$
DECLARE
  criteria_count INT;
  task_type_count INT;
  devlog_count INT;
  link_count INT;
  living_count INT;
  trackable_count INT;
BEGIN
  SELECT COUNT(*) INTO criteria_count FROM criteria_type_catalog;
  SELECT COUNT(*) INTO task_type_count FROM task_type_catalog;
  SELECT COUNT(*) INTO devlog_count FROM devlog_category_catalog;
  SELECT COUNT(*) INTO link_count FROM link_type_catalog;
  SELECT COUNT(*) INTO living_count FROM living_doc_source_catalog;
  SELECT COUNT(*) INTO trackable_count FROM trackable_type_catalog;
  
  RAISE NOTICE '========================================';
  RAISE NOTICE 'SEED COMPLETADO - VTT V4 CATÁLOGOS v2.0';
  RAISE NOTICE '========================================';
  RAISE NOTICE 'criteria_type_catalog: % registros', criteria_count;
  RAISE NOTICE 'task_type_catalog: % registros', task_type_count;
  RAISE NOTICE 'devlog_category_catalog: % registros', devlog_count;
  RAISE NOTICE 'link_type_catalog: % registros', link_count;
  RAISE NOTICE 'living_doc_source_catalog: % registros', living_count;
  RAISE NOTICE 'trackable_type_catalog: % registros', trackable_count;
  RAISE NOTICE '========================================';
END $$;
