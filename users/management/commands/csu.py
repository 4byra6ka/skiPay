from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            phone='+77777777777',
            first_name='Admin',
            last_name='Admin',
            is_staff=True,
            is_superuser=True

        )

        user.set_password('12345')
        user.save()
