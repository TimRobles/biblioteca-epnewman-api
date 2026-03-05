# Biblioteca EP Newman - API Backend

Backend API para la aplicación de Biblioteca EP Newman, desarrollado con Django REST Framework.

## 🚀 Características

- API RESTful con Django REST Framework
- Sistema de gestión de libros (CRUD completo)
- Sistema de alquileres con extensión de plazo
- Búsqueda y filtros por múltiples campos
- Documentación automática con Swagger (drf-spectacular)
- CORS configurado para frontend en Vercel
- Listo para deploy en VPS

## 📋 Requisitos

- Python 3.11+
- PostgreSQL (producción) o SQLite (desarrollo)

## 🛠️ Instalación Local

### 1. Clonar repositorio
```bash
git clone https://github.com/TimRobles/biblioteca-epnewman-api.git
cd biblioteca-epnewman-api
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus valores
```

### 5. Ejecutar migraciones
```bash
python manage.py migrate
```

### 6. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 7. Cargar datos de prueba
```bash
python manage.py loaddata fixtures/books.json
```

### 8. Ejecutar servidor
```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000/api/`

## 📚 Endpoints Principales

### Libros
- `GET /api/books/` - Listar libros (con búsqueda y filtros)
- `POST /api/books/` - Crear libro
- `GET /api/books/{id}/` - Detalle de libro
- `PUT/PATCH /api/books/{id}/` - Actualizar libro
- `DELETE /api/books/{id}/` - Eliminar libro

**Parámetros de búsqueda:**
- `search` - Buscar por título, autor, descripción
- `category` - Filtrar por categoría
- `available` - Filtrar por disponibilidad (true/false)
- `author` - Filtrar por autor

### Alquileres
- `GET /api/rentals/` - Listar alquileres
- `POST /api/rentals/` - Crear alquiler (alquilar libro)
- `GET /api/rentals/{id}/` - Detalle de alquiler
- `PATCH /api/rentals/{id}/extend/` - Extender plazo de alquiler
- `PATCH /api/rentals/{id}/return/` - Devolver libro

## 📖 Documentación API

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- Schema JSON: `http://localhost:8000/api/schema/`

## 🌐 Deploy en VPS

### Configuración para epnewman.regalistos.com.pe

1. Instalar dependencias del sistema:
```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql nginx
```

2. Configurar PostgreSQL
3. Configurar Gunicorn
4. Configurar Nginx como reverse proxy
5. Configurar SSL con Let's Encrypt

## 🔒 Seguridad

- SECRET_KEY en variable de entorno
- DEBUG=False en producción
- ALLOWED_HOSTS configurado
- CORS restringido a dominios específicos
- PostgreSQL en producción (no SQLite)

## 📝 Modelos

### Book
- title (string)
- author (string)
- isbn (string, único)
- isbn13 (string, opcional)
- category (string)
- description (text)
- cover_url (URL)
- year (integer)
- language (string)
- available (boolean)

### Rental
- book (FK a Book)
- user_name (string)
- rented_at (datetime)
- due_at (datetime)
- returned_at (datetime, nullable)
- status (choices: active, returned, overdue)

## 👨‍💻 Desarrollo

Creado por: Tim Robles
Fecha: Marzo 2026
Proyecto: Actividad de Diseño Web Integral
