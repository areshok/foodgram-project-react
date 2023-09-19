import subprocess
import os
from dotenv import load_dotenv


from django.core.management.base import BaseCommand

from user.models import User

load_dotenv()


class Command(BaseCommand):
    help = 'Первоначальная настройка'

    def handle(self, *args, **options):
        base_db()
        #create_superuser()
        #create_stetick()




def base_db():
    #subprocess.call(['python', 'manage.py', 'makemigrations'])
    subprocess.call(['python', 'manage.py', 'migrate'])


def create_stetick():
    subprocess.call(['python', 'manage.py', 'collectstatic'])
    subprocess.call(['cp', '-r', '/app/collected_static/.', '/backend_static/django_static/'])

def create_superuser():
    user = User.objects.create_user(
        username=os.getenv('ADMIN_USERNAME'),
        email=os.getenv('ADMIN_EMAIL'),
        password=os.getenv('ADMIN_PASSWORD'),)
    user.is_superuser=True
    user.is_staff=True
    user.save()


