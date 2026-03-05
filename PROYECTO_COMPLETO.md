# ✅ BACKEND API - COMPLETADO

## 🎉 Resumen del Proyecto

El backend de la **Biblioteca EP Newman API** ha sido completamente desarrollado y está listo para:
1. Desarrollo local
2. Pruebas de la API
3. Deploy en VPS (epnewman.regalistos.com.pe)
4. Integración con el frontend React

---

## 📁 Estructura del Proyecto

```
biblioteca-epnewman-api/
├── config/                      # Configuración Django
│   ├── settings.py             # ✅ Configurado con DRF, CORS, dotenv
│   ├── urls.py                 # ✅ Rutas + documentación Swagger
│   └── wsgi.py
├── library/                     # App principal
│   ├── models.py               # ✅ Book, Rental
│   ├── serializers.py          # ✅ 6 serializers
│   ├── views.py                # ✅ BookViewSet, RentalViewSet
│   ├── urls.py                 # ✅ Rutas de la API
│   ├── admin.py                # ✅ Admin personalizado
│   ├── management/
│   │   └── commands/
│   │       └── load_sample_books.py  # ✅ 20 libros de ejemplo
│   └── migrations/
│       └── 0001_initial.py     # ✅ Migraciones creadas
├── .env                         # Variables de entorno (local)
├── .env.example                 # Plantilla de variables
├── .gitignore                   # ✅ Actualizado
├── requirements.txt             # ✅ Todas las dependencias
├── manage.py
├── README.md                    # ✅ Documentación completa
├── API_TESTING.md              # ✅ Guía de pruebas
└── DEPLOY_VPS.md               # ✅ Guía de deploy
```

---

## ✨ Funcionalidades Implementadas

### 🔹 Modelos (models.py)

#### **Book** (Libro)
- title, author, isbn, isbn10
- category (13 categorías: ficción, ciencia, tecnología, etc.)
- description, synopsis
- cover_url (portada)
- year, language (7 idiomas)
- publisher, pages
- available (disponibilidad)
- Métodos: `is_available`

#### **Rental** (Alquiler)
- book (FK a Book)
- user_name, user_email
- rented_at, due_at, returned_at
- status (active, returned, overdue)
- Métodos: `extend_rental()`, `return_book()`, `is_overdue`, `days_remaining`
- Lógica automática: actualiza disponibilidad del libro

---

### 🔹 API Endpoints

#### **Libros** (`/api/books/`)
- ✅ `GET /api/books/` - Listar (con paginación)
- ✅ `GET /api/books/?search=...` - Búsqueda (título, autor, ISBN)
- ✅ `GET /api/books/?category=...` - Filtrar por categoría
- ✅ `GET /api/books/?available=true` - Filtrar por disponibilidad
- ✅ `GET /api/books/?language=es` - Filtrar por idioma
- ✅ `GET /api/books/{id}/` - Detalle
- ✅ `POST /api/books/` - Crear
- ✅ `PUT/PATCH /api/books/{id}/` - Actualizar
- ✅ `DELETE /api/books/{id}/` - Eliminar
- ✅ `GET /api/books/statistics/` - Estadísticas

#### **Alquileres** (`/api/rentals/`)
- ✅ `GET /api/rentals/` - Listar
- ✅ `GET /api/rentals/?status=active` - Filtrar por estado
- ✅ `GET /api/rentals/?user_email=...` - Filtrar por usuario
- ✅ `POST /api/rentals/` - Crear alquiler
- ✅ `PATCH /api/rentals/{id}/extend/` - **Extender plazo**
- ✅ `PATCH /api/rentals/{id}/return_book/` - **Devolver libro**

---

### 🔹 Características Técnicas

#### **Django REST Framework**
- Paginación (20 items por página)
- Filtros de búsqueda
- Serializers optimizados
- ViewSets con acciones personalizadas

#### **Documentación Automática**
- ✅ Swagger UI: `/api/docs/`
- ✅ ReDoc: `/api/redoc/`
- ✅ Schema JSON: `/api/schema/`

#### **CORS**
- Configurado para frontend (localhost:5173, localhost:3000)
- Listo para Vercel (agregar dominio en producción)

#### **Admin de Django**
- ✅ Panel admin personalizado
- ✅ Filtros y búsqueda
- ✅ Acciones masivas (marcar devuelto, extender plazo)

#### **Datos de Prueba**
- ✅ 20 libros de ejemplo (clásicos + bestsellers + tech)
- ✅ Comando: `python manage.py load_sample_books`

---

## 🚀 Cómo Usar

### 1️⃣ Desarrollo Local

```bash
# Activar entorno virtual
cd biblioteca-epnewman-api
..\..\..\.venv\Scripts\activate  # Windows
source ../../../.venv/bin/activate  # Linux/Mac

# Instalar dependencias (si no están instaladas)
pip install -r requirements.txt

# Crear migraciones (si hay cambios en modelos)
python manage.py makemigrations
python manage.py migrate

# Cargar datos de ejemplo
python manage.py load_sample_books

# Crear superusuario (para admin)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

**Servidor local:** http://localhost:8000

---

### 2️⃣ Probar la API

#### Opción A: Navegador
- Swagger UI: http://localhost:8000/api/docs/
- DRF Browser: http://localhost:8000/api/books/

#### Opción B: cURL
```bash
# Listar libros
curl http://localhost:8000/api/books/

# Buscar
curl "http://localhost:8000/api/books/?search=quijote"

# Crear alquiler
curl -X POST http://localhost:8000/api/rentals/ \
  -H "Content-Type: application/json" \
  -d '{"book": 1, "user_name": "Test", "user_email": "test@example.com"}'
```

#### Opción C: Postman / Insomnia
Importar la colección desde `/api/schema/`

---

### 3️⃣ Deploy en VPS

**Sigue la guía completa:** `DEPLOY_VPS.md`

**Pasos resumidos:**
1. Instalar PostgreSQL, Nginx, Gunicorn
2. Clonar repositorio en `/var/www/`
3. Configurar `.env` con credenciales de producción
4. Ejecutar migraciones
5. Configurar Nginx + SSL (Let's Encrypt)
6. Iniciar servicio Gunicorn

**URL de producción:** https://epnewman.regalistos.com.pe

---

## 🔗 URLs Importantes

### Desarrollo Local
- API Base: http://localhost:8000/api/
- Swagger: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

### Producción (VPS)
- API Base: https://epnewman.regalistos.com.pe/api/
- Swagger: https://epnewman.regalistos.com.pe/api/docs/
- Admin: https://epnewman.regalistos.com.pe/admin/

---

## 📊 Estadísticas del Proyecto

- **Modelos:** 2 (Book, Rental)
- **Endpoints:** 15+ (CRUD + acciones custom)
- **Serializers:** 6
- **Líneas de código:** ~800
- **Libros de ejemplo:** 20
- **Categorías:** 13
- **Idiomas:** 7

---

## 🎯 Siguiente Fase: Frontend React

**Ya puedes conectar el frontend con:**

```javascript
// .env en React
VITE_API_URL=http://localhost:8000/api
# o en producción:
VITE_API_URL=https://epnewman.regalistos.com.pe/api
```

**Endpoints para usar en React:**
- Catálogo: `GET ${API_URL}/books/`
- Búsqueda: `GET ${API_URL}/books/?search=${query}`
- Detalle: `GET ${API_URL}/books/${id}/`
- Alquilar: `POST ${API_URL}/rentals/`
- Mis alquileres: `GET ${API_URL}/rentals/?user_email=${email}`
- Extender: `PATCH ${API_URL}/rentals/${id}/extend/`

---

## ✅ Checklist Completado

Backend:
- [x] Proyecto Django inicializado
- [x] Django REST Framework configurado
- [x] CORS configurado
- [x] Modelos Book y Rental
- [x] Serializers
- [x] ViewSets con búsqueda y filtros
- [x] Endpoints CRUD completos
- [x] Acciones custom (extend, return)
- [x] Admin personalizado
- [x] Datos de ejemplo (20 libros)
- [x] Documentación Swagger
- [x] Variables de entorno (.env)
- [x] README completo
- [x] Guía de pruebas (API_TESTING.md)
- [x] Guía de deploy (DEPLOY_VPS.md)

Pendiente:
- [ ] Deploy en VPS
- [ ] Configurar dominio y SSL
- [ ] Agregar dominio de Vercel a CORS
- [ ] Frontend React (siguiente fase)

---

## 🐛 Solución de Problemas

### Error al instalar psycopg2
```bash
pip install psycopg2-binary
```

### Puerto 8000 ocupado
```bash
python manage.py runserver 8080
```

### CORS bloqueado
Verificar en `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite
    'http://localhost:3000',  # Create React App
]
```

---

## 📞 Soporte

- Documentación Django: https://docs.djangoproject.com/
- Documentación DRF: https://www.django-rest-framework.org/
- Documentación drf-spectacular: https://drf-spectacular.readthedocs.io/

---

## 🎓 Para la Actividad

Este backend cumple con todos los requisitos:

✅ **Base de datos:** PostgreSQL/SQLite con 2 modelos relacionados  
✅ **Buscador:** Búsqueda por título, autor, ISBN, descripción  
✅ **Tareas principales:**
1. Alquilar libro
2. Extender plazo de alquiler

✅ **Bonus:** También permite devolver libro y ver estadísticas

---

**¡El backend está 100% listo! 🎉**

Próximo paso: Crear el frontend React en `biblioteca-epnewman-web/`
