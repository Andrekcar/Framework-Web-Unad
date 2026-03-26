# Impulsa Local - UNAD
**Curso:** Framework para el desarrollo web - Código: 202047928  
**Fase 3:** Diseño y planeación tecnológica del proyecto web


---

## Tecnologías utilizadas:

- Python 3.x
- Django 6.0
- python-dotenv
- SQLite

---

## Requisitos previos

- Python 3.x instalado
- Git instalado
- Editor de código (VS Code, PyCharm, etc.)

> Si optas por **GitHub Codespaces**, no necesitas instalar nada.

---

## Configuración del entorno

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd nombre-del-proyecto
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia la plantilla de ejemplo, crea el archivo .env:

```bash
cp .env.example .env
```

Abre el archivo `.env` 

### 4. Generar tu propia SECRET_KEY

> ⚠️ Cada integrante debe generar su propia clave.

Ejecuta este comando y copia la llave en la variable del archivo `.env`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

`.env` deberia quedar así:

```
SECRET_KEY=aqui-va-tu-llave-generada
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

Abre tu navegador en: [http://127.0.0.1:8000]

---

## Evidencia individual (Paso 3)

Cada integrante debe:

1. Configurar su propio entorno siguiendo los pasos anteriores
2. Crear una página simple que muestre su nombre
3. Tomar captura de pantalla del servidor corriendo y la página en el navegador
4. Publicar la evidencia en el foro de la actividad


---

## Estructura del proyecto

```
FRAMEWORK-WEB-UNAD/       ← carpeta raíz del repositorio
├── manage.py
├── requirements.txt
├── .env.example          ← plantilla de variables de entorno 
├── .env                  ← valores reales (aqui va la llave generada, se debe crear el archivo)
├── .gitignore
├── README.md
├── db.sqlite3            ← base de datos local
├── templates/            ← archivos HTML 
├── core/                 ← app Django
└── impulsa_local/        ← proyecto Django
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

---

## Notas importantes

- El archivo `.env` **nunca** debe subirse al repositorio
- Cada integrante genera su propia `SECRET_KEY` para su entorno local
- En producción se usaría una `SECRET_KEY` única y segura gestionada por el equipo
- Cualquier duda comentar por el grupo de Whatsapp
