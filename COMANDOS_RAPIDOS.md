# 🚀 Comandos Rápidos - Backend API

## Desarrollo Local

### Iniciar servidor
```bash
cd biblioteca-epnewman-api
python manage.py runserver
```

### Crear migraciones (después de cambiar modelos)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Cargar datos de ejemplo
```bash
python manage.py load_sample_books
```

### Crear superusuario
```bash
python manage.py createsuperuser
```

### Shell interactivo de Django
```bash
python manage.py shell
```

---

## Pruebas Rápidas

### Ver todos los libros
```bash
curl http://localhost:8000/api/books/
```

### Buscar libros
```bash
curl "http://localhost:8000/api/books/?search=quijote"
```

### Filtrar por categoría
```bash
curl "http://localhost:8000/api/books/?category=ficcion"
```

### Ver estadísticas
```bash
curl http://localhost:8000/api/books/statistics/
```

### Crear alquiler
```bash
curl -X POST http://localhost:8000/api/rentals/ \
  -H "Content-Type: application/json" \
  -d '{"book": 1, "user_name": "Test User", "user_email": "test@example.com"}'
```

---

## URLs Importantes

- **API:** http://localhost:8000/api/
- **Swagger:** http://localhost:8000/api/docs/
- **Admin:** http://localhost:8000/admin/
- **Libros:** http://localhost:8000/api/books/
- **Alquileres:** http://localhost:8000/api/rentals/

---

## Deploy en VPS

### Actualizar código
```bash
cd /var/www/biblioteca-epnewman-api
./update.sh
```

### Ver logs
```bash
# Gunicorn
tail -f /var/log/gunicorn/error.log

# Nginx
tail -f /var/log/nginx/biblioteca-error.log
```

### Reiniciar servicios
```bash
sudo systemctl restart gunicorn-biblioteca
sudo systemctl restart nginx
```

---

## Gestión de Base de Datos

### Backup (PostgreSQL)
```bash
pg_dump biblioteca_epnewman > backup_$(date +%Y%m%d).sql
```

### Restaurar
```bash
psql biblioteca_epnewman < backup_20260305.sql
```

### Ver libros en la BD
```bash
python manage.py shell
>>> from library.models import Book
>>> Book.objects.count()
>>> Book.objects.all()
```

---

## Git

### Commit y push
```bash
git add .
git commit -m "Descripción del cambio"
git push origin main
```

### Ver estado
```bash
git status
```

---

## Solución Rápida de Problemas

### Puerto ocupado
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux
lsof -ti:8000 | xargs kill -9
```

### Reinstalar dependencias
```bash
pip install -r requirements.txt --force-reinstall
```

### Limpiar migraciones (CUIDADO: borra la BD)
```bash
python manage.py flush
python manage.py migrate
python manage.py load_sample_books
```
