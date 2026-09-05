# Script to fix social media icons
from django.core.management.base import BaseCommand
from core.models import SocialMedia

class Command(BaseCommand):
    help = 'Fix social media icons'

    def handle(self, *args, **options):
        # Mapping platform to correct Font Awesome icon
        icon_mapping = {
            'instagram': 'fab fa-instagram',
            'tiktok': 'fab fa-tiktok',
            'github': 'fab fa-github',
            'saweria': 'fas fa-donate',  # Saweria doesn't have a specific icon
            'email': 'fas fa-envelope',
            'whatsapp': 'fab fa-whatsapp',
        }
        
        socials = SocialMedia.objects.all()
        self.stdout.write(f'\nTotal social media to fix: {socials.count()}\n')
        
        for social in socials:
            old_icon = social.icon
            if social.platform in icon_mapping:
                social.icon = icon_mapping[social.platform]
                social.save()
                self.stdout.write(f'Updated {social.platform} icon from "{old_icon}" to "{social.icon}"')
            else:
                self.stdout.write(f'Platform {social.platform} not found in mapping, icon not updated')
        
        self.stdout.write(self.style.SUCCESS('\nSocial media icons fixed successfully!\n'))