if __name__ == '__main__':
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    django.setup()

    from django.contrib.auth.models import User

    username = os.getenv('SUPERUSER_USERNAME', 'Admin')
    password = os.getenv('SUPERUSER_PASSWORD', 'Admin123')
    
    if not User.objects.filter(username = username).exists():
        User.objects.create_superuser(
            username = username,
            email = None,
            password = password
        )
        print(f"super user '{username}' created.")
    else:
        print(f"super user '{username}' already exists.")
