from .models import SiteSettings

def site_settings(request):
    """Context processor to make site_settings available in all templates"""
    site_settings = SiteSettings.objects.first() or SiteSettings.objects.create()
    return {
        'site_settings': site_settings
    }