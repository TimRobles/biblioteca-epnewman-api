# Guía de Pruebas de la API

## 🚀 Servidor en ejecución

El servidor debe estar corriendo en: `http://localhost:8000`

## 📚 Endpoints Disponibles

### **Libros (Books)**

#### 1. Listar todos los libros
```bash
GET http://localhost:8000/api/books/
```

#### 2. Buscar libros (por título, autor, descripción, ISBN)
```bash
GET http://localhost:8000/api/books/?search=quijote
GET http://localhost:8000/api/books/?search=garcía
GET http://localhost:8000/api/books/?search=978
```

#### 3. Filtrar por categoría
```bash
GET http://localhost:8000/api/books/?category=ficcion
GET http://localhost:8000/api/books/?category=ciencia
GET http://localhost:8000/api/books/?category=tecnologia
```

#### 4. Filtrar por disponibilidad
```bash
GET http://localhost:8000/api/books/?available=true
GET http://localhost:8000/api/books/?available=false
```

#### 5. Filtrar por idioma
```bash
GET http://localhost:8000/api/books/?language=es
GET http://localhost:8000/api/books/?language=en
```

#### 6. Combinación de filtros
```bash
GET http://localhost:8000/api/books/?category=ficcion&available=true&language=es
```

#### 7. Obtener detalle de un libro
```bash
GET http://localhost:8000/api/books/1/
```

#### 8. Crear un libro (POST)
```bash
POST http://localhost:8000/api/books/
Content-Type: application/json

{
  "title": "Nuevo Libro",
  "author": "Autor Ejemplo",
  "isbn": "9781234567890",
  "category": "ficcion",
  "description": "Descripción del libro",
  "year": 2024,
  "language": "es"
}
```

#### 9. Obtener estadísticas
```bash
GET http://localhost:8000/api/books/statistics/
```

---

### **Alquileres (Rentals)**

#### 1. Listar todos los alquileres
```bash
GET http://localhost:8000/api/rentals/
```

#### 2. Filtrar por estado
```bash
GET http://localhost:8000/api/rentals/?status=active
GET http://localhost:8000/api/rentals/?status=returned
GET http://localhost:8000/api/rentals/?status=overdue
```

#### 3. Filtrar por email de usuario
```bash
GET http://localhost:8000/api/rentals/?user_email=usuario@example.com
```

#### 4. Crear un alquiler (alquilar libro)
```bash
POST http://localhost:8000/api/rentals/
Content-Type: application/json

{
  "book": 1,
  "user_name": "Juan Pérez",
  "user_email": "juan@example.com",
  "notes": "Primer alquiler"
}
```

#### 5. Extender plazo de alquiler
```bash
PATCH http://localhost:8000/api/rentals/1/extend/
Content-Type: application/json

{
  "days": 7
}
```

#### 6. Devolver libro
```bash
PATCH http://localhost:8000/api/rentals/1/return_book/
```

---

## 🔍 Documentación Interactiva

### Swagger UI (Recomendado)
```
http://localhost:8000/api/docs/
```
Interfaz interactiva donde puedes probar todos los endpoints directamente desde el navegador.

### ReDoc
```
http://localhost:8000/api/redoc/
```
Documentación alternativa con mejor diseño para lectura.

### Schema JSON
```
http://localhost:8000/api/schema/
```
Esquema OpenAPI en formato JSON.

---

## 👨‍💻 Panel de Administración

```
http://localhost:8000/admin/
```

**Crear superusuario:**
```bash
python manage.py createsuperuser
```

---

## 🧪 Probar con cURL

### Obtener lista de libros
```bash
curl http://localhost:8000/api/books/
```

### Buscar libros
```bash
curl "http://localhost:8000/api/books/?search=quijote"
```

### Crear alquiler
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "book": 1,
    "user_name": "Test User",
    "user_email": "test@example.com"
  }'
```

---

## 📊 Casos de Prueba Completos

### Flujo 1: Buscar y alquilar un libro

1. **Buscar libros de ficción disponibles:**
   ```
   GET /api/books/?category=ficcion&available=true
   ```

2. **Ver detalle del libro elegido (ID 2, por ejemplo):**
   ```
   GET /api/books/2/
   ```

3. **Alquilar el libro:**
   ```
   POST /api/rentals/
   {
     "book": 2,
     "user_name": "María García",
     "user_email": "maria@example.com"
   }
   ```

4. **Verificar que el libro ya no está disponible:**
   ```
   GET /api/books/2/
   ```
   (El campo `available` debería ser `false`)

### Flujo 2: Extender y devolver alquiler

1. **Ver mis alquileres:**
   ```
   GET /api/rentals/?user_email=maria@example.com
   ```

2. **Extender plazo del alquiler (ID 1):**
   ```
   PATCH /api/rentals/1/extend/
   {
     "days": 14
   }
   ```

3. **Devolver el libro:**
   ```
   PATCH /api/rentals/1/return_book/
   ```

4. **Verificar que el libro está disponible de nuevo:**
   ```
   GET /api/books/2/
   ```
   (El campo `available` debería ser `true`)

---

## ✅ Verificaciones

- [ ] El servidor corre sin errores en `http://localhost:8000`
- [ ] Los libros de ejemplo se cargan correctamente (20 libros)
- [ ] La búsqueda funciona correctamente
- [ ] Los filtros funcionan (categoría, idioma, disponibilidad)
- [ ] Se puede crear un alquiler
- [ ] Al alquilar, el libro se marca como no disponible
- [ ] Se puede extender un alquiler
- [ ] Se puede devolver un alquiler
- [ ] Al devolver, el libro se marca como disponible
- [ ] La documentación Swagger funciona
- [ ] El admin de Django funciona

---

## 🐛 Solución de Problemas

### El servidor no inicia
```bash
# Verificar que estás en el directorio correcto
cd biblioteca-epnewman-api

# Verificar que el entorno virtual está activado
..\..\.venv\Scripts\activate

# Iniciar servidor
python manage.py runserver
```

### No hay libros en la base de datos
```bash
python manage.py load_sample_books
```

### Error de CORS al llamar desde el frontend
Verificar que en `.env` o `settings.py` está configurado:
```python
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```
