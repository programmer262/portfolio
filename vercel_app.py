import os
from django.core.wsgi import get_wsgi_application

# Replace 'portfolio' with the actual name of your inner Django configuration folder
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

app = get_wsgi_application()
