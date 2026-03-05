# Guía de Deploy en VPS (epnewman.regalistos.com.pe)

Esta guía te ayudará a desplegar el backend de la Biblioteca EP Newman en tu VPS.

## 📋 Requisitos Previos

- VPS con Ubuntu 20.04+ o similar
- Acceso SSH al servidor
- Dominio: `epnewman.regalistos.com.pe` apuntando a tu VPS
- Python 3.10+
- PostgreSQL
- Nginx

---

## 🚀 Paso 1: Preparar el Servidor

### 1.1 Conectar al VPS via SSH
```bash
ssh tu_usuario@epnewman.regalistos.com.pe
```

### 1.2 Actualizar el sistema
```bash
sudo apt update
sudo apt upgrade -y
```

### 1.3 Instalar dependencias del sistema
```bash
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y nginx
sudo apt install -y git
sudo apt install -y certbot python3-certbot-nginx
```

---

## 🗄️ Paso 2: Configurar PostgreSQL

### 2.1 Crear usuario y base de datos
```bash
sudo -u postgres psql
```

Dentro de PostgreSQL:
```sql
CREATE DATABASE biblioteca_epnewman;
CREATE USER biblioteca_user WITH PASSWORD 'tu_password_seguro_aqui';
ALTER ROLE biblioteca_user SET client_encoding TO 'utf8';
ALTER ROLE biblioteca_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE biblioteca_user SET timezone TO 'America/Lima';
GRANT ALL PRIVILEGES ON DATABASE biblioteca_epnewman TO biblioteca_user;
\q
```

---

## 📦 Paso 3: Clonar y Configurar el Proyecto

### 3.1 Crear directorio para la aplicación
```bash
sudo mkdir -p /var/www
cd /var/www
```

### 3.2 Clonar el repositorio
```bash
sudo git clone https://github.com/TimRobles/biblioteca-epnewman-api.git
sudo chown -R $USER:$USER biblioteca-epnewman-api
cd biblioteca-epnewman-api
```

### 3.3 Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.4 Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### 3.5 Crear archivo de variables de entorno
```bash
nano .env
```

Contenido del archivo `.env`:
```env
SECRET_KEY=genera-una-clave-secreta-muy-larga-y-segura-aqui
DEBUG=False
ALLOWED_HOSTS=epnewman.regalistos.com.pe,www.epnewman.regalistos.com.pe

# PostgreSQL
DATABASE_URL=postgresql://biblioteca_user:tu_password_seguro_aqui@localhost:5432/biblioteca_epnewman

# CORS (agrega el dominio de Vercel cuando lo tengas)
CORS_ALLOWED_ORIGINS=https://biblioteca-epnewman.vercel.app,https://www.biblioteca-epnewman.vercel.app
```

**Generar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3.6 Actualizar settings.py para usar PostgreSQL

Editar `config/settings.py` y reemplazar la sección de DATABASES:

```python
import os
import dj_database_url

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}
```

Instalar `dj-database-url`:
```bash
pip install dj-database-url
```

### 3.7 Ejecutar migraciones
```bash
python manage.py migrate
python manage.py load_sample_books
python manage.py collectstatic --noinput
```

### 3.8 Crear superusuario
```bash
python manage.py createsuperuser
```

---

## 🔧 Paso 4: Configurar Gunicorn

### 4.1 Crear archivo de configuración de Gunicorn
```bash
nano /var/www/biblioteca-epnewman-api/gunicorn_config.py
```

Contenido:
```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"
```

### 4.2 Crear directorio de logs
```bash
sudo mkdir -p /var/log/gunicorn
sudo chown -R $USER:$USER /var/log/gunicorn
```

### 4.3 Crear servicio systemd para Gunicorn
```bash
sudo nano /etc/systemd/system/gunicorn-biblioteca.service
```

Contenido:
```ini
[Unit]
Description=Gunicorn daemon for Biblioteca EP Newman API
After=network.target

[Service]
User=tu_usuario
Group=www-data
WorkingDirectory=/var/www/biblioteca-epnewman-api
Environment="PATH=/var/www/biblioteca-epnewman-api/venv/bin"
ExecStart=/var/www/biblioteca-epnewman-api/venv/bin/gunicorn \
          --config /var/www/biblioteca-epnewman-api/gunicorn_config.py \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Reemplaza `tu_usuario` con tu nombre de usuario.

### 4.4 Iniciar y habilitar el servicio
```bash
sudo systemctl start gunicorn-biblioteca
sudo systemctl enable gunicorn-biblioteca
sudo systemctl status gunicorn-biblioteca
```

---

## 🌐 Paso 5: Configurar Nginx

### 5.1 Crear configuración de Nginx
```bash
sudo nano /etc/nginx/sites-available/biblioteca-epnewman
```

Contenido:
```nginx
server {
    listen 80;
    server_name epnewman.regalistos.com.pe www.epnewman.regalistos.com.pe;

    # Logs
    access_log /var/log/nginx/biblioteca-access.log;
    error_log /var/log/nginx/biblioteca-error.log;

    # Static files
    location /static/ {
        alias /var/www/biblioteca-epnewman-api/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/biblioteca-epnewman-api/media/;
        expires 7d;
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # CORS headers (opcional, Django ya los maneja)
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, PATCH, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization' always;
    }

    # Aumentar tamaño máximo de upload
    client_max_body_size 10M;
}
```

### 5.2 Activar el sitio
```bash
sudo ln -s /etc/nginx/sites-available/biblioteca-epnewman /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 Paso 6: Configurar SSL con Let's Encrypt

### 6.1 Obtener certificado SSL
```bash
sudo certbot --nginx -d epnewman.regalistos.com.pe -d www.epnewman.regalistos.com.pe
```

Sigue las instrucciones en pantalla.

### 6.2 Renovación automática
Certbot debería configurar la renovación automática. Puedes verificar:
```bash
sudo certbot renew --dry-run
```

---

## 🔄 Paso 7: Scripts de Actualización

### 7.1 Crear script de actualización
```bash
nano /var/www/biblioteca-epnewman-api/update.sh
```

Contenido:
```bash
#!/bin/bash

echo "Actualizando Biblioteca EP Newman API..."

# Navegar al directorio del proyecto
cd /var/www/biblioteca-epnewman-api

# Activar entorno virtual
source venv/bin/activate

# Obtener últimos cambios
git pull origin main

# Instalar/actualizar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Reiniciar Gunicorn
sudo systemctl restart gunicorn-biblioteca

echo "¡Actualización completada!"
```

Dar permisos de ejecución:
```bash
chmod +x /var/www/biblioteca-epnewman-api/update.sh
```

### 7.2 Uso del script
```bash
cd /var/www/biblioteca-epnewman-api
./update.sh
```

---

## 📊 Paso 8: Monitoreo y Logs

### Ver logs de Gunicorn
```bash
tail -f /var/log/gunicorn/error.log
tail -f /var/log/gunicorn/access.log
```

### Ver logs de Nginx
```bash
tail -f /var/log/nginx/biblioteca-error.log
tail -f /var/log/nginx/biblioteca-access.log
```

### Ver estado del servicio
```bash
sudo systemctl status gunicorn-biblioteca
```

### Reiniciar servicios
```bash
sudo systemctl restart gunicorn-biblioteca
sudo systemctl restart nginx
```

---

## ✅ Verificación Final

1. **Verificar que la API responde:**
   ```bash
   curl https://epnewman.regalistos.com.pe/api/books/
   ```

2. **Acceder a la documentación:**
   - https://epnewman.regalistos.com.pe/api/docs/

3. **Acceder al admin:**
   - https://epnewman.regalistos.com.pe/admin/

4. **Probar CORS desde el navegador:**
   Abre la consola del navegador en cualquier sitio y ejecuta:
   ```javascript
   fetch('https://epnewman.regalistos.com.pe/api/books/')
     .then(r => r.json())
     .then(console.log)
   ```

---

## 🔧 Solución de Problemas

### Error 502 Bad Gateway
```bash
sudo systemctl status gunicorn-biblioteca
tail -f /var/log/gunicorn/error.log
```

### Error de permisos en static files
```bash
sudo chown -R $USER:www-data /var/www/biblioteca-epnewman-api
sudo chmod -R 755 /var/www/biblioteca-epnewman-api/staticfiles
```

### Base de datos no conecta
Verificar credenciales en `.env` y que PostgreSQL esté corriendo:
```bash
sudo systemctl status postgresql
```

### CORS no funciona
1. Verificar que el dominio de Vercel esté en `CORS_ALLOWED_ORIGINS` en `.env`
2. Reiniciar Gunicorn: `sudo systemctl restart gunicorn-biblioteca`

---

## 📝 Notas Importantes

1. **Backups**: Configura backups automáticos de PostgreSQL
2. **Firewall**: Asegúrate de que solo los puertos 80, 443 y 22 estén abiertos
3. **Actualizaciones**: Mantén el sistema y las dependencias actualizadas
4. **Monitoreo**: Considera usar herramientas como Sentry para rastrear errores

---

## 🎯 Próximos Pasos

Una vez que el backend esté desplegado:

1. Anota la URL base de tu API: `https://epnewman.regalistos.com.pe`
2. Úsala como `VITE_API_URL` en tu frontend de React
3. Actualiza `CORS_ALLOWED_ORIGINS` con el dominio de Vercel donde despliegues el frontend
4. ¡Listo para conectar el frontend!
