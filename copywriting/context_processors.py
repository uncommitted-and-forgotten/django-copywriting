
def disqus_shortname(request):
    from django.conf import settings
    
    return {'disqus_shortname' : settings.DISQUS_SHORTNAME}
