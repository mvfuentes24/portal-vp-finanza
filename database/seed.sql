-- =====================================================================
-- Portal VP de Finanzas — Datos semilla (ficticios)
-- Ejecutar DESPUÉS de schema.sql:
--   psql -U portal_app -d portal_finanzas -f database/seed.sql
--
-- =====================================================================

SET client_encoding = 'UTF8';

BEGIN;

-- =====================================================================
-- 1. CATÁLOGOS
-- =====================================================================

INSERT INTO paises (id, nombre) VALUES
    (1, 'Venezuela'),
    (2, 'Argentina'),
    (3, 'Colombia');

INSERT INTO niveles (id, nombre) VALUES
    (1, 'Junior'),
    (2, 'Semi-senior'),
    (3, 'Senior'),
    (4, 'Gerente'),
    (5, 'Vicepresidente');

-- =====================================================================
-- 2. DEPARTAMENTOS DE LA VP DE FINANZAS
-- =====================================================================

INSERT INTO departamentos (id, nombre, descripcion) VALUES
    (1, 'Planificación Financiera', 'Elabora el presupuesto y hace seguimiento a su ejecución'),
    (2, 'Tesorería',                'Administra el efectivo, los pagos y las cuentas bancarias'),
    (3, 'Contraloría',              'Vela por el control interno y revisa irregularidades en la operación'),
    (4, 'Contabilidad',             'Registra las operaciones y elabora los estados financieros');

-- =====================================================================
-- 3. CARGOS
--    Cada departamento tiene 4 cargos, uno por nivel.
-- =====================================================================

INSERT INTO cargos (id, nombre, nivel_id, departamento_id) VALUES
    -- Vicepresidencia
    (17, 'Vicepresidente de Finanzas',                 5, NULL),
    -- Planificación Financiera
    (1,  'Gerente de Planificación Financiera',        4, 1),
    (2,  'Analista de Planificación Financiera Senior', 3, 1),
    (3,  'Analista de Presupuesto Semi-senior',        2, 1),
    (4,  'Analista de Presupuesto Junior',             1, 1),
    -- Tesorería
    (5,  'Gerente de Tesorería',                       4, 2),
    (6,  'Analista de Tesorería Senior',               3, 2),
    (7,  'Analista de Tesorería Semi-senior',          2, 2),
    (8,  'Analista de Tesorería Junior',               1, 2),
    -- Contraloría
    (9,  'Gerente de Contraloría',                     4, 3),
    (10, 'Auditor Interno Senior',                     3, 3),
    (11, 'Analista de Control Interno Semi-senior',    2, 3),
    (12, 'Analista de Control Interno Junior',         1, 3),
    -- Contabilidad
    (13, 'Gerente de Contabilidad',                    4, 4),
    (14, 'Contador Senior',                            3, 4),
    (15, 'Analista Contable Semi-senior',              2, 4),
    (16, 'Analista Contable Junior',                   1, 4);

-- =====================================================================
-- 4. FUNCIONES Y SU ASIGNACIÓN A CARGOS
-- =====================================================================

INSERT INTO funciones (id, descripcion) VALUES
    -- Comunes a las gerencias
    (1,  'Elaborar reportes de gestión para la Vicepresidencia'),
    (2,  'Supervisar y evaluar al equipo del departamento'),
    (3,  'Aprobar los entregables del departamento'),
    -- Planificación Financiera
    (4,  'Elaborar el presupuesto anual'),
    (5,  'Hacer seguimiento a la ejecución presupuestaria'),
    (6,  'Preparar proyecciones financieras'),
    (7,  'Consolidar la información de las áreas para el presupuesto'),
    -- Tesorería
    (8,  'Gestionar los pagos a proveedores'),
    (9,  'Elaborar el flujo de caja semanal'),
    (10, 'Conciliar cuentas bancarias'),
    (11, 'Registrar los movimientos bancarios'),
    -- Contraloría
    (12, 'Planificar y ejecutar auditorías internas'),
    (13, 'Revisar las alertas de anomalías en cierres de caja'),
    (14, 'Evaluar los controles internos de los procesos'),
    (15, 'Documentar los hallazgos de auditoría'),
    -- Contabilidad
    (16, 'Elaborar los estados financieros'),
    (17, 'Registrar los asientos contables'),
    (18, 'Preparar las declaraciones de impuestos'),
    (19, 'Realizar el cierre contable mensual'),
    -- Vicepresidencia
    (20, 'Definir la estrategia financiera de la Vicepresidencia'),
    (21, 'Aprobar el presupuesto anual');

INSERT INTO cargo_funciones (cargo_id, funcion_id) VALUES
    -- Vicepresidente
    (17, 1), (17, 20), (17, 21),
    -- Gerentes: funciones comunes de gerencia
    (1, 1), (1, 2), (1, 3),
    (5, 1), (5, 2), (5, 3),
    (9, 1), (9, 2), (9, 3),
    (13, 1), (13, 2), (13, 3),
    -- Planificación Financiera
    (2, 4), (2, 5), (2, 6),
    (3, 4), (3, 5),
    (4, 5), (4, 7),
    -- Tesorería (la conciliación bancaria también la hace Contabilidad)
    (6, 8), (6, 9),
    (7, 8), (7, 9), (7, 10),
    (8, 10), (8, 11),
    -- Contraloría (todos revisan alertas de cierres de caja)
    (10, 12), (10, 13), (10, 14),
    (11, 13), (11, 14), (11, 15),
    (12, 13), (12, 15),
    -- Contabilidad
    (14, 16), (14, 18), (14, 19),
    (15, 10), (15, 17), (15, 18), (15, 19),
    (16, 17), (16, 19);

-- =====================================================================
-- 5. COLABORADORES
--    Vicepresidente + 10 por departamento.
--    Por departamento: 1 gerente, 2 senior, 3 semi-senior, 4 junior.
--    Cada departamento tiene un colaborador inactivo.
-- =====================================================================

INSERT INTO colaboradores (id, nombre, apellido, correo, pais_id, fecha_ingreso, estado, cargo_id) VALUES
    -- Vicepresidencia
    (41, 'Elisa',     'Montero',   'elisa.montero@vpfinanzas.example',      1, '2012-02-06', 'activo',   17),
    -- Planificación Financiera
    (1,  'Andrea',    'Salazar',   'andrea.salazar@vpfinanzas.example',     1, '2016-03-14', 'activo',   1),
    (2,  'Ricardo',   'Méndez',    'ricardo.mendez@vpfinanzas.example',     1, '2018-07-02', 'activo',   2),
    (3,  'Valeria',   'Ortiz',     'valeria.ortiz@vpfinanzas.example',      3, '2019-01-21', 'activo',   2),
    (4,  'Gabriel',   'Rojas',     'gabriel.rojas@vpfinanzas.example',      1, '2021-05-10', 'activo',   3),
    (5,  'Daniela',   'Cárdenas',  'daniela.cardenas@vpfinanzas.example',   2, '2022-02-01', 'activo',   3),
    (6,  'José',      'Pineda',    'jose.pineda@vpfinanzas.example',        1, '2020-09-15', 'inactivo', 3),
    (7,  'Mariana',   'Quintero',  'mariana.quintero@vpfinanzas.example',   1, '2024-01-08', 'activo',   4),
    (8,  'Luis',      'Herrera',   'luis.herrera@vpfinanzas.example',       3, '2024-06-17', 'activo',   4),
    (9,  'Camila',    'Duarte',    'camila.duarte@vpfinanzas.example',      2, '2025-03-03', 'activo',   4),
    (10, 'Tomás',     'Aguilera',  'tomas.aguilera@vpfinanzas.example',     1, '2025-09-22', 'activo',   4),
    -- Tesorería
    (11, 'Patricia',  'Montilla',  'patricia.montilla@vpfinanzas.example',  1, '2015-11-09', 'activo',   5),
    (12, 'Fernando',  'Lugo',      'fernando.lugo@vpfinanzas.example',      1, '2017-04-24', 'activo',   6),
    (13, 'Isabel',    'Navas',     'isabel.navas@vpfinanzas.example',       2, '2019-08-12', 'activo',   6),
    (14, 'Diego',     'Paredes',   'diego.paredes@vpfinanzas.example',      1, '2021-02-15', 'activo',   7),
    (15, 'Natalia',   'Villalobos','natalia.villalobos@vpfinanzas.example', 1, '2022-06-06', 'activo',   7),
    (16, 'Andrés',    'Guerrero',  'andres.guerrero@vpfinanzas.example',    3, '2022-10-03', 'activo',   7),
    (17, 'Sofía',     'Benítez',   'sofia.benitez@vpfinanzas.example',      2, '2023-03-20', 'inactivo', 8),
    (18, 'Martín',    'Cabrera',   'martin.cabrera@vpfinanzas.example',     2, '2024-05-13', 'activo',   8),
    (19, 'Lucía',     'Sosa',      'lucia.sosa@vpfinanzas.example',         1, '2025-01-27', 'activo',   8),
    (20, 'Javier',    'Ramírez',   'javier.ramirez@vpfinanzas.example',     1, '2025-07-14', 'activo',   8),
    -- Contraloría
    (21, 'Carolina',  'Briceño',   'carolina.briceno@vpfinanzas.example',   1, '2014-08-18', 'activo',   9),
    (22, 'Alejandro', 'Torres',    'alejandro.torres@vpfinanzas.example',   1, '2017-10-30', 'activo',   10),
    (23, 'Elena',     'Machado',   'elena.machado@vpfinanzas.example',      2, '2018-12-03', 'activo',   10),
    (24, 'Héctor',    'Figueroa',  'hector.figueroa@vpfinanzas.example',    1, '2020-04-06', 'activo',   11),
    (25, 'Paula',     'Ríos',      'paula.rios@vpfinanzas.example',         3, '2021-09-13', 'activo',   11),
    (26, 'Sebastián', 'Molina',    'sebastian.molina@vpfinanzas.example',   2, '2022-01-24', 'activo',   11),
    (27, 'Adriana',   'Castillo',  'adriana.castillo@vpfinanzas.example',   1, '2023-08-07', 'activo',   12),
    (28, 'Emilio',    'Fajardo',   'emilio.fajardo@vpfinanzas.example',     1, '2023-02-13', 'inactivo', 12),
    (29, 'Verónica',  'Alvarado',  'veronica.alvarado@vpfinanzas.example',  2, '2024-10-21', 'activo',   12),
    (30, 'Nicolás',   'Peralta',   'nicolas.peralta@vpfinanzas.example',    1, '2025-05-05', 'activo',   12),
    -- Contabilidad
    (31, 'Gustavo',   'Linares',   'gustavo.linares@vpfinanzas.example',    1, '2013-06-10', 'activo',   13),
    (32, 'Mónica',    'Suárez',    'monica.suarez@vpfinanzas.example',      1, '2016-09-26', 'activo',   14),
    (33, 'Raúl',      'Espinoza',  'raul.espinoza@vpfinanzas.example',      3, '2019-03-11', 'activo',   14),
    (34, 'Teresa',    'Gallardo',  'teresa.gallardo@vpfinanzas.example',    1, '2020-11-16', 'activo',   15),
    (35, 'Óscar',     'Medina',    'oscar.medina@vpfinanzas.example',       2, '2021-07-19', 'activo',   15),
    (36, 'Laura',     'Becerra',   'laura.becerra@vpfinanzas.example',      1, '2022-12-05', 'activo',   15),
    (37, 'Pablo',     'Acosta',    'pablo.acosta@vpfinanzas.example',       1, '2023-11-27', 'activo',   16),
    (38, 'Juliana',   'Ferrer',    'juliana.ferrer@vpfinanzas.example',     3, '2024-04-15', 'activo',   16),
    (39, 'Manuel',    'Prieto',    'manuel.prieto@vpfinanzas.example',      1, '2025-02-10', 'activo',   16),
    (40, 'Beatriz',   'Salas',     'beatriz.salas@vpfinanzas.example',      2, '2023-06-26', 'inactivo', 16);

-- =====================================================================
-- 6. MÓDULO DE CIERRES DE CAJA
--    Adaptado del dataset de ejemplo "Caso 1" de la prueba técnica:
--    - El país de cada tienda pasa a referenciar la tabla paises.
-- =====================================================================

INSERT INTO tiendas (id, nombre, pais_id) VALUES
    (1, 'Tienda Chacao',           1),
    (2, 'Tienda Las Mercedes',     1),
    (3, 'Tienda Maracaibo Centro', 1),
    (4, 'Tienda Palermo',          2),
    (5, 'Tienda Belgrano',         2),
    (6, 'Tienda Córdoba Norte',    2);

INSERT INTO cajeros (id, nombre, tienda_id) VALUES
    (1,  'Rosa Delgado',       3),
    (2,  'Miguel Ochoa',       2),
    (3,  'Yelitza Bravo',      4),
    (4,  'Franklin Uzcátegui', 6),
    (5,  'Carla Beltrán',      1),
    (6,  'Hugo Sandoval',      1),
    (7,  'Ana Bracho',         5),
    (8,  'Wilmer Colmenares',  1),
    (9,  'Estefanía Requena',  3),
    (10, 'Bruno Villalba',     5),
    (11, 'Marcos Ledesma',     1),
    (12, 'Rocío Funes',        5);

-- registrado_por queda en NULL: estos cierres provienen de la carga
-- inicial del dataset, no de un usuario del portal.
INSERT INTO cierres_caja (id, tienda_id, cajero_id, fecha, monto_declarado, monto_sistema) VALUES
    ( 1, 6,  4, '2026-06-03',   959.20,   961.79),
    ( 2, 3,  9, '2026-06-28',   759.62,   755.15),
    ( 3, 1, 11, '2026-07-11',  4789.94,  4789.08),
    ( 4, 3,  1, '2026-06-15',  1152.09,   658.69),
    ( 5, 3,  9, '2026-06-08',  4697.86,  4696.04),
    ( 6, 2,  2, '2026-07-08',  4694.24,  4698.27),
    ( 7, 5, 12, '2026-06-05',  4645.60,  4645.64),
    ( 8, 3,  9, '2026-06-28',  6288.89,  6284.66),
    ( 9, 1,  6, '2026-06-20',  2215.68,  2212.88),
    (10, 2,  2, '2026-07-07',  2610.35,  2611.92),
    (11, 1,  8, '2026-06-19',  4989.10,  4988.98),
    (12, 4,  3, '2026-06-22',  1465.67,  1470.28),
    (13, 1, 11, '2026-06-05',  6190.95,  6187.20),
    (14, 1,  6, '2026-06-22',  5654.57,  5653.77),
    (15, 1,  8, '2026-06-05',  6947.75,  6767.75),
    (16, 5, 12, '2026-07-13',   800.50,   800.50),
    (17, 1, 11, '2026-07-07',  8648.48,  7946.84),
    (18, 1, 11, '2026-06-23',   470.41,   473.73),
    (19, 2,  2, '2026-07-02',   573.95,   753.95),
    (20, 5, 12, '2026-06-16',  3620.22,  3363.81),
    (21, 1,  8, '2026-06-26',  5335.48,  4530.69),
    (22, 1,  5, '2026-07-16',  3501.62,  3497.78),
    (23, 6,  4, '2026-06-10',   940.57,   938.98),
    (24, 3,  1, '2026-07-02',  6697.24,  6699.42),
    (25, 4,  3, '2026-06-27',  4414.54,  4416.35),
    (26, 4,  3, '2026-07-15',  6765.86,  6915.86),
    (27, 1,  8, '2026-07-14',  6442.61,  6443.62),
    (28, 2,  2, '2026-07-01',  5179.70,  5184.03),
    (29, 6,  4, '2026-06-29',  1545.26,  1549.73),
    (30, 3,  1, '2026-07-07',  1463.38,  1464.74),
    (31, 3,  1, '2026-06-05',  7028.85,  7032.36),
    (32, 1,  5, '2026-06-23',  4933.70,  4937.55),
    (33, 1,  8, '2026-06-30',  3995.48,  3999.04),
    (34, 5, 12, '2026-06-22',  6002.62,  6000.70),
    (35, 3,  9, '2026-06-02',  1700.16,  1880.16),
    (36, 4,  3, '2026-07-15',  4482.71,  4482.43),
    (37, 1, 11, '2026-06-06',  5659.39,  5660.72),
    (38, 4,  3, '2026-06-23',  6246.71,  6243.92),
    (39, 1,  6, '2026-07-11',  1253.16,  2017.42),
    (40, 5,  7, '2026-06-15',  1841.68,  1839.37),
    (41, 3,  1, '2026-06-18',  3937.30,  3936.25),
    (42, 1,  6, '2026-06-29',  6255.96,  6525.96),
    (43, 1,  6, '2026-06-06',  1994.53,  1997.56),
    (44, 6,  4, '2026-07-01',  4569.68,  5105.31),
    (45, 1, 11, '2026-06-23',  6458.87,  6457.26),
    (46, 5,  7, '2026-07-16',  6072.87,  6076.08),
    (47, 1, 11, '2026-06-22',  1147.97,   967.97),
    (48, 1,  8, '2026-06-26',  6020.41,  6023.82),
    (49, 4,  3, '2026-06-02',   835.76,  1463.86),
    (50, 5, 10, '2026-07-01',  5361.46,  5360.97),
    (51, 4,  3, '2026-06-02',   259.67,   409.67),
    (52, 3,  9, '2026-06-09',  3420.73,  3640.33),
    (53, 6,  4, '2026-06-19',  4518.95,  4158.95),
    (54, 1,  5, '2026-07-05',  3530.50,  3526.40),
    (55, 1,  6, '2026-06-30',  6180.06,  5401.06),
    (56, 3,  9, '2026-06-09',  4390.24,  4395.05),
    (57, 1,  8, '2026-06-12',  9485.87,  4985.87),
    (58, 4,  3, '2026-06-10',  3954.90,  3945.90),
    (59, 3,  1, '2026-06-21',  5553.77,  5553.95),
    (60, 2,  2, '2026-07-06',   732.95,   737.53);

-- Fecha de registro: se toma la fecha del cierre (la carga inicial no tiene hora real)
UPDATE cierres_caja SET registrado_en = fecha;

-- =====================================================================
-- 7. SINCRONIZAR LAS SECUENCIAS DE IDENTIDAD
--    Como se insertaron ids explícitos, se ajusta cada contador para que
--    el próximo registro creado desde el portal continúe la numeración.
-- =====================================================================

SELECT setval(pg_get_serial_sequence('paises', 'id'),        (SELECT MAX(id) FROM paises));
SELECT setval(pg_get_serial_sequence('niveles', 'id'),       (SELECT MAX(id) FROM niveles));
SELECT setval(pg_get_serial_sequence('departamentos', 'id'), (SELECT MAX(id) FROM departamentos));
SELECT setval(pg_get_serial_sequence('cargos', 'id'),        (SELECT MAX(id) FROM cargos));
SELECT setval(pg_get_serial_sequence('funciones', 'id'),     (SELECT MAX(id) FROM funciones));
SELECT setval(pg_get_serial_sequence('colaboradores', 'id'), (SELECT MAX(id) FROM colaboradores));
SELECT setval(pg_get_serial_sequence('tiendas', 'id'),       (SELECT MAX(id) FROM tiendas));
SELECT setval(pg_get_serial_sequence('cajeros', 'id'),       (SELECT MAX(id) FROM cajeros));
SELECT setval(pg_get_serial_sequence('cierres_caja', 'id'),  (SELECT MAX(id) FROM cierres_caja));

COMMIT;