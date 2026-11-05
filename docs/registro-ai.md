# Registro de uso de AI

Este documento registra cómo se usó inteligencia artificial en el desarrollo del Portal
Corporativo de Finanzas: qué se le pidió, qué sugerencias se aceptaron, cuáles se modificaron o
rechazaron, y los errores de la AI que se detectaron y corrigieron.

## Herramienta y forma de trabajo

- **Herramienta:** Claude (Anthropic).
- **Forma de trabajo:** el proyecto se construyó paso a paso. Antes de aceptar cada parte (modelo
  de datos, reglas, seguridad, pantallas) se le pidió a la AI que explicara qué hacía y por qué, y
  en qué parte del enunciado se basaba.
- **Verificación:** cada sugerencia se contrastó con el enunciado, con la documentación del dataset
  y con los datos reales del dataset. El código se validó con pruebas automatizadas (pytest), con
  el compilador de TypeScript y probando las pantallas con cada rol.
- **Seguridad de la información:** a la AI no se le compartieron contraseñas, claves, el archivo
  `.env` ni datos reales de personas o de la empresa. Cuando hacía falta un valor sensible se usó un
  marcador (por ejemplo, `tu_contraseña`), y todos los datos del proyecto son ficticios.

## Prompts representativos

| Etapa | Prompt (resumido o textual) | Para qué |
|---|---|---|
| Planificación | "¿Qué herramientas recomiendas?" / "Usaré React y FastAPI." | Elegir el stack. |
| Base de datos | "Explícame bien el problema y la decisión 1." | Entender cada restricción antes de aceptarla. |
| Base de datos |  Cuestionar el diseño de cargos y niveles. |
| Roles | "El administrador, ¿quién podría ser? | Definir los usuarios y el rol de la VP. |
| Reglas | "1. Por porcentaje de 1 %… 4. No hagas esa alerta… ¿Sale una alerta si se pasa del 1 %?" | Decidir las reglas de detección y sus parámetros. |
| Seguridad | "¿Qué es JWT_SECRET_KEY?" / "¿El .env.example es público?" | Manejar secretos correctamente. |
| Frontend | "Puedes arreglar que esas etiquetas no se vean encima de las otras." | Corregir errores visuales encontrados al probar. |

## Sugerencias aceptadas

| Sugerencia | Por qué se aceptó |
|---|---|
| Arquitectura por módulos con capas `router`, `service`, `repository`, `models` y `schemas`. | Separa responsabilidades y deja cada regla en un lugar predecible. |
| Centralizar los permisos en `core/permissions.py`. | Un solo lugar que revisar; las reglas se aplican igual en todos los módulos. |
| Sesión con JWT en una cookie `httpOnly`, con solo el id del usuario. | El token no queda expuesto al JavaScript de la página y los cambios de rol tienen efecto inmediato. |
| Mensaje genérico de error al iniciar sesión, con tiempo de respuesta igualado. | No revela qué correos existen. |
| Usuario de base de datos `portal_app` sin privilegios de administrador. | Principio de mínimo privilegio. |
| El cargo de Vicepresidente sin departamento, con un índice único parcial. | Refleja la estructura real y evita que otros cargos queden sin departamento por error. |
| Reglas de detección como funciones puras. | Se prueban aisladas y los umbrales están en un solo lugar. |
| Pruebas dentro de una transacción que se deshace. | Se pueden repetir sin alterar la base de datos local. |
| Proxy de Vite para que frontend y backend compartan origen. | La cookie de sesión funciona sin configuración entre dominios. |

## Sugerencias modificadas

| Sugerencia original | Cambio | Motivo |
|---|---|---|
| Usar Alembic para crear la base de datos. | Se usaron dos scripts SQL (`schema.sql` y `seed.sql`). | Para este alcance son más fáciles de leer, revisar y ejecutar. Alembic quedó como mejora a futuro. |
| Una tabla `lugares` jerárquica, que era la propuesta de la autora. | Se mantuvo `paises`. | El enunciado solo necesita el país. La tabla jerárquica quedó documentada como mejora. |

## Sugerencias rechazadas

| Sugerencia | Motivo del rechazo |
|---|---|
| Detectar la transposición de dígitos con el atajo "la diferencia es múltiplo de 9". | Es una condición necesaria pero no suficiente. En el dataset marcaría como transposición los cierres 15, 35 y 47, que no lo son. Se compara dígito a dígito y solo se aceptan dígitos contiguos. |

## Errores de la AI detectados

### 1. Presentar una interpretación como regla oficial

**Qué pasó:** la AI propuso `UNIQUE (cajero_id, fecha)` en `cierres_caja` y lo presentó como una
regla del enunciado.

**Cómo se detectó:** la autora preguntó dónde lo decía la documentación. La documentación del
dataset dice "un cierre por cajero/fecha", pero el propio dataset tiene 6 pares de cierres con el
mismo cajero y la misma fecha, y el comentario del archivo SQL habla de "ese turno".

**Corrección:** no se agregó la restricción, porque los datos no la cumplen, ni una regla que
trate los repetidos como anomalía. La inconsistencia quedó documentada como limitación.

### 2. Historial de alertas desactualizado

**Qué pasó:** en el código de gestión de alertas, después de cambiar el estado la respuesta
devolvía el historial sin el último cambio.

**Cómo se detectó:** una prueba automatizada verificaba que el último registro del historial fuera
el cambio recién hecho, y falló.

**Corrección:** el nuevo registro se agrega a través de la relación de la alerta, de modo que la
respuesta incluye el historial completo.


### 3. Pruebas que dependían del estado de la base de datos

**Qué pasó:** algunas pruebas fallaban si en la base local ya se habían registrado cierres a mano,
porque contaban todas las alertas y usaban fechas que podían chocar con esos cierres.

**Cómo se detectó:** al ejecutar las pruebas después de probar el portal manualmente.

**Corrección:** las pruebas del dataset filtran solo los cierres originales y los cierres de
prueba usan una fecha fija fuera del rango de los datos.

### 4. Errores visuales

**Qué pasó:** algunos estilos generados rompían las tablas (fechas y encabezados partidos en
varias líneas) y las etiquetas de alerta se encimaban cuando una celda tenía dos.

**Cómo se detectó:** la autora los vio al probar las pantallas y los reportó con capturas.

**Corrección:** fechas, montos y encabezados en una sola línea, y separación uniforme entre
etiquetas.

## Conclusión

La AI aceleró el trabajo en la estructura del código, las explicaciones y el diseño de las
pantallas. Pero las decisiones de negocio (qué reglas aplicar, qué datos usar, quién es la
administradora, qué hacer con las inconsistencias del dataset) se tomaron verificando contra el
enunciado y los datos. Varios errores solo se detectaron gracias a esa verificación y a las
pruebas automatizadas, por lo que ninguna sugerencia se aceptó sin revisarla.
