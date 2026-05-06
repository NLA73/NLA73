import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_project.settings')
django.setup()

from app.models import User
from django.contrib.auth.hashers import make_password

count = 0
for user in User.objects.all():
    # Check if the password lacks the standard django hash prefix
    if not user.password.startswith('pbkdf2_') and not user.password.startswith('argon2'):
        user.password = make_password(user.password)
        user.save()
        print(f"Fixed hashed password for {user.username}")
        count += 1

print(f"Fixed {count} user passwords.")
