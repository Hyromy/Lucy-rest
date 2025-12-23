# Lucy Rest

API REST con Django Rest Framework para [Lucy](https://github.com/Hyromy/Lucy)

![Django](https://img.shields.io/badge/Django-6.0-green?logo=django)
![DRF](https://img.shields.io/badge/DRF-3.16.1-red?logo=django)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)

## Índice
- [Lucy Rest](#lucy-rest)
  - [Índice](#índice)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Variables de entrono](#variables-de-entrono)
  - [Despliegue](#despliegue)
    - [Local](#local)
    - [Docker](#docker)

## Estructura del proyecto

Se posee una estructura típica de un proyecto de Django

```sh
app/                  # aplicación principal
├── migrations/       # migraciones
│
├── models.py         # modelos
├── serializers.py    # serializadores
├── urls.py           # rutas de aplicación
└── views.py          # enpoints

project/              # proyecto principal
├── settings.py       # configuración del proyecto
└── urls.py           # rutas

manage.py             # script de comandos Django
requirements.txt      # dependencias
```

## Variables de entrono

Aunque el proyecto puede funcionar sin establecer ninguna variable de entorno, puedes configurar el `.env` con las variables de entorno disponibles.

| Clave | Valor por defecto | Descripción |
| - | - | - |
| `PRODUCTION` | `False` | Establece si el modo es de producción |
| `DJANGO_SECRET_KEY` | `"secret"` | Secret de seguridad |
| `PG_DB` | `"postgres"` | Base de datos PostgreSQL |
| `PG_USER` | `"postgres"` | Usuario de PostgreSQL |
| `PG_PASS` | `"postgres"` | Contraseña de PostgreSQL |
| `PG_HOST` | `"localhost"` | Host de PostgreSQL |
| `PG_POST` | `5432` | Puerto de PostgreSQL |
| `SUPERUSER_USERNAME` | `Admin` | Super usuario de la aplicación |
| `SUPERUSER_PASSWORD` | `Admin123` | Contraseña del super usuario |

## Despliegue

### Local

1. Entorno virtual
   
   Crea un entorno virtual, como ejemplo se usa el módulo `venv`.
   ```sh
   py -m venv env
   ```

   Activa el entorno virtual.
   ```sh
   .\env\Scripts\activate     # Windows
   ```

2. Dependencias
   
   Instala las [dependencias](./requirements.txt).
   ```sh
   pip install -r requirements.txt
   ```

3. Migraciones
   
   Aplica las migraciones.
   ```sh
   py manage.py migrate
   ```

El proyecto se ejecuta en el puerto `8000` pero puedes especificar otro.

```sh
py manage.py runserver          # port 8000

py manage.py runserver 7001     # port 7001
```

---

### Docker

Puedes construir una imagen y contenedor con el [Dockerfile](./Dockerfile).
```sh
docker build -t app_image .

docker run --name app_container -p 8000:8000 app_image
```

Por último puedes ejecutar un entorno pre-producción sin ninguna [variable de entorno](#variables-de-entrono).
```sh
docker compose up
```
