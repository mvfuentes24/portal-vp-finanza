# Portal Corporativo de Finanzas

Portal web interno para la Vicepresidencia de Finanzas. Permite consultar la estructura de la
organización (departamentos, cargos y colaboradores) y detectar anomalías en los cierres de caja
de las tiendas, con acceso controlado por roles.


## Funcionalidades

| Módulo | Descripción |
|---|---|
| Inicio de sesión | Acceso con correo y contraseña. La sesión se guarda en una cookie `httpOnly`. |
| Organización | Departamentos de la Vicepresidencia y los colaboradores de cada uno. |
| Cargos | Ficha de cada cargo: nivel, departamento, funciones y colaboradores que lo ocupan. |
| Cierres de caja | Registro de cierres y detección automática de anomalías: diferencias fuera de rango, posible transposición de dígitos y reincidencia de un cajero. Las alertas se gestionan con un historial de cambios. |

### Roles

| Rol | Acceso |
|---|---|
| Administrador | Toda la información del portal y todos los módulos. |
| Jefe de departamento | Información de su departamento. Si su departamento es Contraloría, también registra cierres y gestiona alertas. |
| Colaborador | Directorio de su departamento y su propio perfil. Si pertenece a Contraloría, puede consultar cierres y alertas, pero no modificarlos. |

Los permisos se validan en el backend; el frontend solo oculta lo que el usuario no puede usar.

## Tecnologías

- **Base de datos:** PostgreSQL
- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic, PyJWT, pwdlib (Argon2)
- **Frontend:** React, TypeScript, Vite, Material UI
- **Pruebas:** pytest

## Requisitos

- PostgreSQL 15 o superior
- Python 3.11 o superior
- Node.js 20.19 o superior (o 22.12 o superior)
- Git

## Instalación y ejecución local

Los comandos están escritos para PowerShell en Windows. En Linux o macOS, cambia la activación
del entorno virtual por `source .venv/bin/activate`.

### 1. Clonar el repositorio

```powershell
git clone https://github.com/<usuario>/<repositorio>.git
cd <repositorio>
```

### 2. Crear la base de datos

Conéctate a PostgreSQL con un usuario administrador (por ejemplo `postgres`):

```powershell
psql -U postgres
```

Crea el usuario de la aplicación y la base de datos. Reemplaza `tu_contraseña` por una propia:

```sql
CREATE ROLE portal_app WITH LOGIN PASSWORD 'tu_contraseña';
CREATE DATABASE portal_finanzas OWNER portal_app ENCODING 'UTF8' TEMPLATE template0;
\q
```

La aplicación usa el usuario `portal_app`, sin privilegios de administrador, en lugar de `postgres`.

### 3. Crear las tablas y cargar los datos de ejemplo

Desde la raíz del repositorio:

```powershell
psql -U portal_app -d portal_finanzas -f database/schema.sql
psql -U portal_app -d portal_finanzas -f database/seed.sql
```

### 4. Configurar las variables de entorno

```powershell
Copy-Item .env.example .env
```

Abre `.env` y completa:

- `DB_PASSWORD`: la contraseña que definiste para `portal_app`.
- `JWT_SECRET_KEY`: una clave aleatoria larga. Puedes generarla con
  `python -c "import secrets; print(secrets.token_urlsafe(64))"`.
- `DEMO_PASSWORD`: la contraseña que tendrán los usuarios de prueba (mínimo 12 caracteres).

El archivo `.env` no se sube al repositorio.

### 5. Instalar el backend y preparar los datos

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
python -m scripts.crear_usuarios
python -m scripts.analizar_cierres
```

- `crear_usuarios` crea los usuarios de prueba con la contraseña de `DEMO_PASSWORD`.
- `analizar_cierres` revisa los cierres cargados y genera sus alertas.

Los dos scripts se pueden ejecutar más de una vez sin duplicar datos.

Si PowerShell bloquea la activación del entorno virtual, ejecuta una vez
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### 6. Iniciar el backend

Con el entorno virtual activo, dentro de `backend`:

```powershell
uvicorn app.main:app --reload
```

La API queda en http://localhost:8000. Su documentación interactiva está en http://localhost:8000/docs.

### 7. Instalar e iniciar el frontend

En otra terminal, desde la raíz del repositorio:

```powershell
cd frontend
npm install
npm run dev
```

Abre http://localhost:5173 e inicia sesión con alguno de los usuarios de prueba.

## Usuarios de prueba

Todos usan la contraseña definida en `DEMO_PASSWORD`.

| Correo | Rol | Departamento |
|---|---|---|
| elisa.montero@vpfinanzas.example | Administrador | Vicepresidencia (Vicepresidente de Finanzas) |
| andrea.salazar@vpfinanzas.example | Jefe de departamento | Planificación Financiera |
| patricia.montilla@vpfinanzas.example | Jefe de departamento | Tesorería |
| carolina.briceno@vpfinanzas.example | Jefe de departamento | Contraloría |
| gustavo.linares@vpfinanzas.example | Jefe de departamento | Contabilidad |
| mariana.quintero@vpfinanzas.example | Colaborador | Planificación Financiera |
| diego.paredes@vpfinanzas.example | Colaborador | Tesorería |
| hector.figueroa@vpfinanzas.example | Colaborador | Contraloría |
| pablo.acosta@vpfinanzas.example | Colaborador | Contabilidad |
| emilio.fajardo@vpfinanzas.example | Colaborador inactivo | Contraloría (no puede iniciar sesión) |

## Pruebas

Con el entorno virtual activo, dentro de `backend`:

```powershell
pytest
```

Las pruebas cubren el inicio de sesión, el control de acceso por rol, las reglas de detección y
la gestión de alertas. Cada prueba corre dentro de una transacción que se deshace al terminar,
así que no modifican los datos de la base local. Necesitan los datos de ejemplo y los usuarios de
prueba ya creados (pasos 3 y 5).

## Estructura del proyecto

```
├── database/
│   ├── schema.sql          Tablas, restricciones e índices
│   └── seed.sql            Datos ficticios de ejemplo
├── backend/
│   ├── app/
│   │   ├── core/           Configuración, base de datos, seguridad y permisos
│   │   └── modules/        auth, organizacion, cargos, cierres_caja
│   ├── scripts/            Creación de usuarios y análisis inicial de cierres
│   └── tests/
├── frontend/
│   └── src/
│       ├── api/            Cliente HTTP y tipos
│       ├── auth/           Sesión del usuario
│       ├── components/     Componentes compartidos
│       └── modules/        Una carpeta por pantalla o módulo
├── docs/
│   ├── decisiones-tecnicas.md
│   └── registro-ai.md
└── .env.example
```

Cada módulo del backend se divide en `router` (endpoints), `service` (reglas de negocio),
`repository` (consultas), `models` (tablas) y `schemas` (datos de entrada y salida).

## Documentación

- [Decisiones técnicas](docs/decisiones-tecnicas.md)
- [Registro de uso de AI](docs/registro-ai.md)
