import os
import sys

# File ini digunakan untuk deployment di cPanel dengan Passenger WSGI
# JANGAN mengubah file ini kecuali Anda tahu apa yang Anda lakukan

# Tambahkan direktori proyek ke sys.path
# Ini memastikan Python dapat menemukan modul-modul di direktori parent
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

# Tambahkan direktori aplikasi ke sys.path
# Ini memastikan Python dapat menemukan modul-modul di direktori saat ini
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

# Setel pengaturan Django
# Menentukan modul settings yang akan digunakan (biolink.settings)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biolink.settings')

# Impor aplikasi Django
# Membuat instance WSGI application yang akan digunakan oleh server web
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()  # Variabel 'application' digunakan oleh Passenger WSGI