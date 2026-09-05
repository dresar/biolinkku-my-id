# Script to check social media data
from django.core.management.base import BaseCommand
from core.models import SocialMedia

class Command(BaseCommand):
    help = 'Check social media data'

    def handle(self, *args, **options):
        socials = SocialMedia.objects.all()
        self.stdout.write(f'\nTotal social media: {socials.count()}\n')
        
        for s in socials:
            self.stdout.write(f'Platform: {s.platform}, Icon: {s.icon}, Active: {s.is_active}')