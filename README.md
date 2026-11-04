# Portal VP de Finanzas

![Estado](https://img.shields.io/badge/estado-en%20desarrollo-yellow)
![Backend](https://img.shields.io/badge/backend-FastAPI-009688)
![Frontend](https://img.shields.io/badge/frontend-React-61DAFB)
![Base de datos](https://img.shields.io/badge/BD-PostgreSQL-336791)

Portal interno para la Vicepresidencia de Finanzas que centraliza la consulta de la estructura organizacional, controla el acceso a la información según el rol y el departamento de cada usuario, e incorpora un detector de anomalías en cierres de caja con gestión y trazabilidad de alertas.

---

## Descripción del proyecto

El equipo de Finanzas trabaja a diario con información sensible: estructura organizacional, datos de colaboradores y procesos de control. Este portal ofrece un punto único de acceso a esa información, donde cada usuario ve y opera **únicamente lo que su rol y departamento le permiten**.


## Características

- Inicio de sesión real con contraseñas almacenadas de forma segura
- Control de acceso por rol y departamento, validado en el backend
- Consulta de departamentos, colaboradores y cargos desde una base de datos relacional normalizada
- Módulos visibles según el rol del usuario autenticado
- Detector de anomalías en cierres de caja con historial auditable de alertas *(en desarrollo)*
- Variables sensibles fuera del código fuente mediante `.env`
- Documentación interactiva de la API generada automáticamente

### Roles del sistema

| Rol | Alcance |
|---|---|
| **Administrador** | Acceso a todos los departamentos y módulos |
| **Jefe de Departamento** | Acceso solo a los datos y módulos de su departamento |
| **Colaborador** | Solo lectura de información limitada de su perfil y departamento |

### Módulos del portal

| Módulo | Tipo | Descripción |
|---|---|---|
| **Organización** | Consulta | Departamentos de la VP y sus colaboradores |
| **Cargos** | Consulta | Ficha de cada cargo con sus funciones y nivel |
| **Cierres de caja** | Proceso de negocio | Registro de cierres, detección automática de anomalías y gestión de alertas |

### Detector de anomalías en cierres de caja

Cada cierre de caja compara el monto declarado por el cajero con el monto registrado por el sistema. El detector aplica las siguientes reglas:

- **Diferencia fuera de rango:** la diferencia entre ambos montos supera el umbral permitido.
- **Transposición de dígitos:** los montos contienen los mismos dígitos con dos de ellos intercambiados (por ejemplo, 1250 frente a 1520).
- **Reincidencia:** un mismo cajero acumula varias anomalías.

Cada anomalía genera una alerta que puede estar **pendiente**, **revisada** o **descartada**. Cada cambio de estado queda registrado en un historial con el usuario que lo gestionó, la fecha y un comentario.

*Los parámetros de cada regla se documentarán al completar el módulo.*

## Tecnologías usadas

| Capa | Tecnología | Propósito |
|---|---|---|
| Backend | Python + FastAPI | API REST, autenticación y lógica de negocio |
| Base de datos | PostgreSQL | Almacenamiento relacional |
| Frontend | React + TypeScript (Vite) | Interfaz de usuario |

La justificación de cada elección se encuentra en [docs/decisiones-tecnicas.md](docs/decisiones-tecnicas.md).

## Estructura del proyecto

El proyecto se organiza **por módulos**: cada funcionalidad del portal agrupa sus propias rutas, lógica, acceso a datos y validaciones. Los elementos compartidos (configuración, conexión a la base de datos y seguridad) viven en `core/`.

> Estructura planificada. Se actualizará a medida que avance el desarrollo.

```
portal-vp-finanza/
├── backend/
│   ├── app/
│   │   ├── main.py                  # Inicialización de la aplicación
│   │   ├── core/
│   │   │   ├── config.py            # Lectura y validación de variables de entorno
│   │   │   ├── database.py          # Conexión a PostgreSQL
│   │   │   ├── security.py          # Hash de contraseñas y tokens JWT
│   │   │   └── permissions.py       # Verificación de rol y departamento
│   │   └── modules/
│   │       ├── auth/                # Inicio de sesión
│   │       ├── organizacion/        # Departamentos y colaboradores
│   │       ├── cargos/              # Cargos y funciones
│   │       └── cierres_caja/        # Detector de anomalías en cierres de caja
│   ├── tests/                       # Pruebas automatizadas
│   └── requirements.txt             # Dependencias de Python
├── frontend/
│   └── src/
│       ├── api/                     # Comunicación con el backend
│       ├── auth/                    # Sesión del usuario y rutas protegidas
│       ├── modules/                 # Pantallas de cada módulo
│       ├── components/              # Componentes compartidos
│       └── App.tsx                  # Definición de rutas
├── database/
│   ├── 01_schema.sql                # Creación de tablas, llaves y restricciones
│   └── 02_seed.sql                  # Datos ficticios de prueba
├── docs/
│   ├── decisiones-tecnicas.md       # Justificación de decisiones del proyecto
│   └── registro-ai.md               # Registro de uso de inteligencia artificial
├── .env.example                     # Plantilla de variables de entorno
├── .gitignore                       # Archivos excluidos del control de versiones
└── README.md                        # Este archivo
```

Cada módulo del backend contiene:

| Archivo | Responsabilidad |
|---|---|
| `router.py` | Endpoints HTTP del módulo |
| `service.py` | Lógica de negocio |
| `repository.py` | Acceso a la base de datos |
| `models.py` | Representación de las tablas |
| `schemas.py` | Validación de datos de entrada y salida |

## Flujo típico de una petición protegida

1. El usuario inicia sesión en `POST /auth/login`
   - Se valida la contraseña contra su hash almacenado
   - Se emite un token de sesión
2. El usuario consulta, por ejemplo, los colaboradores de un departamento
   - Se verifica que el token sea válido
   - Se verifica su rol y su departamento
   - Si no tiene permiso, la API responde **403 Prohibido**, sin revelar datos
   - Si tiene permiso, el servicio obtiene los datos a través del repositorio
3. Toda gestión de una alerta queda registrada en el historial: quién, cuándo y qué cambió

## Requisitos previos

Instala lo siguiente antes de comenzar:

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) 3.11 o superior
- [Node.js](https://nodejs.org/) (versión LTS)
- [PostgreSQL](https://www.postgresql.org/) 15 o superior

## Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/mvfuentes24/portal-vp-finanza.git
cd portal-vp-finanza
```

### 2. Crear la base de datos

Conéctate a PostgreSQL como administrador:

```bash
psql -U postgres
```

Ejecuta los siguientes comandos. Cuando se solicite, define una contraseña para el usuario `portal_app` y anótala:

```sql
CREATE ROLE portal_app WITH LOGIN;
\password portal_app
CREATE DATABASE portal_finanzas WITH OWNER = portal_app ENCODING = 'UTF8' TEMPLATE = template0;
\q
```

### 3. Configurar las variables de entorno

Crea el archivo `.env` a partir de la plantilla:

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Abre `.env` y completa:

| Variable | Valor |
|---|---|
| `DB_PASSWORD` | La contraseña definida para `portal_app` en el paso 2 |
| `JWT_SECRET_KEY` | Una cadena aleatoria larga (ver comando abajo) |

Las demás variables ya tienen valores por defecto válidos para ejecución local.

Para generar `JWT_SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

### 4. Crear las tablas y cargar los datos

```bash
psql -U portal_app -d portal_finanzas -f database/01_schema.sql
psql -U portal_app -d portal_finanzas -f database/02_seed.sql
```

### 5. Levantar el backend

*Pendiente.*

### 6. Levantar el frontend

*Pendiente.*

### 7. Abrir el portal

*Pendiente.* Ingresa con alguno de los [usuarios de prueba](#usuarios-de-prueba).

## Usuarios de prueba

*Pendiente.* Se documentarán credenciales ficticias para cada rol.

## Documentación de la API

Con el backend en ejecución, la documentación interactiva está disponible en `http://localhost:8000/docs`.

## Pruebas

*Pendiente.*

## Seguridad

- Credenciales y claves gestionadas mediante variables de entorno, fuera del código fuente
- Conexión a la base de datos con un usuario de privilegios mínimos
- Contraseñas almacenadas como hash, nunca en texto plano *(en desarrollo)*
- Control de acceso verificado en cada endpoint del backend *(en desarrollo)*

El detalle de cada decisión está en [docs/decisiones-tecnicas.md](docs/decisiones-tecnicas.md).

## Documentación adicional

- [Decisiones técnicas](docs/decisiones-tecnicas.md): stack, modelo de datos, proceso de negocio, seguridad y limitaciones
- [Registro de uso de AI](docs/registro-ai.md): prompts principales y sugerencias aceptadas, modificadas y rechazadas

## Autora

**Maria Victoria Fuentes Gutierrez** — [@mvfuentes24](https://github.com/mvfuentes24)
Estudiante de Ingeniería Informática, Universidad Católica Andrés Bello (UCAB).

---

> **Nota sobre los datos:** toda la información de este proyecto es completamente ficticia. No se utilizan nombres, documentos de identidad, correos ni datos de personas o empresas reales.