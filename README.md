

# Impulsa Local - UNAD
**Curso:** Framework para el desarrollo web - Código: 202047928  
**Fase 3:** Diseño y planeación tecnológica del proyecto web

# Guía para Iniciar el Proyecto en su Entorno

Instrucciones paso a paso para ejecutar el proyecto Django localmente o desde GitHub Codespaces.

---

## Requisitos previos

- Python 3.10+ instalado (si se corre localmente)
- Git instalado (si se clona localmente)

---

## Paso 1 — Clonar el repositorio o abrir Codespaces

**Opción A – Clonar localmente:**
```bash
git clone https://github.com/<usuario>/<repositorio>.git
cd <repositorio>
```

**Opción B – Abrir en GitHub Codespaces:**  
Ir al repositorio → botón verde **`<> Code`** → pestaña **Codespaces** → **Create codespace on main**

---

## Paso 2 — Crear el archivo `.env`

En la raíz del proyecto encontrarás el archivo `.env.plantilla`.  
Renómbralo (o cópialo) como `.env`:

---

## Paso 3 — Generar la SECRET_KEY

Dentro del archivo `.env` hay un campo `SECRET_KEY` vacío. Genera una clave segura con el siguiente comando:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y pégalo en el `.env`:

---

## Paso 4 — Aplicar las migraciones

```bash
python manage.py migrate
```

Esto crea la base de datos y todas las tablas necesarias.

---

## Paso 5 — Crear el usuario administrador (superusuario)

```bash
python manage.py createsuperuser
```

El sistema pedirá:
- **Username** (nombre de usuario)
- **Email** (puede dejarse vacío)
- **Password** (y confirmación)

---

## Paso 6 — Correr el servidor de desarrollo

```bash
python manage.py runserver
```

El servidor quedará activo en: `http://127.0.0.1:8000/`

> En Codespaces, el puerto se abrirá automáticamente y recibirás un enlace público generado por GitHub.

---

## Paso 7 — Acceder al panel de administración

En el navegador, agrega `/admin` a la URL base: http://127.0.0.1:8000/admin/

> En Codespaces, usa la URL pública que generó el entorno + `/admin/`

---
