import os
import datetime
from django.conf import settings
import django

# Configurar Django si el script se ejecuta de manera independiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehix.settings')
django.setup()

# Ruta de almacenamiento de backups
BACKUP_DIR = os.path.join(settings.BASE_DIR, 'backups')
os.makedirs(BACKUP_DIR, exist_ok=True)

# Generar nombre del archivo de backup
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.sql")

# Obtener configuración de la base de datos
DB_CONFIG = settings.DATABASES['default']
DB_NAME = DB_CONFIG['NAME']
DB_USER = DB_CONFIG.get('USER', '')
DB_PASSWORD = DB_CONFIG.get('PASSWORD', '')
DB_HOST = DB_CONFIG.get('HOST', 'localhost')

# Generar comando según el motor de base de datos
if DB_CONFIG['ENGINE'] == 'django.db.backends.postgresql':
    command = f'PGPASSWORD="{DB_PASSWORD}" pg_dump -U {DB_USER} -h {DB_HOST} -F c -b -v -f "{backup_file}" {DB_NAME}'
elif DB_CONFIG['ENGINE'] == 'django.db.backends.mysql':
    command = f'mysqldump -u {DB_USER} -p{DB_PASSWORD} -h {DB_HOST} {DB_NAME} > "{backup_file}"'
elif DB_CONFIG['ENGINE'] == 'django.db.backends.sqlite3':
    command = f'cp "{DB_NAME}" "{backup_file}"'
else:
    raise Exception("Motor de base de datos no soportado")

# Ejecutar comando
os.system(command)
print(f"Backup guardado en: {backup_file}")
