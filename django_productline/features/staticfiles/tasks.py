from ape import tasks

@tasks.register
@tasks.requires_product_environment
def prepare_staticfiles(force=False):
    """
    collect static files for production httpd

    If run with ``settings.DEBUG==True``, this is a no-op
    unless ``force`` is set to ``True``
    """
    #noise reduction: only collectstatic if not in debug mode
    from django.conf import settings
    if force or not settings.DEBUG:
        tasks.manage('collectstatic')




def refine_post_context_deploy(original):
    """
    adds call to build_staticfiles
    """
    def deploy():
        original()
        tasks.prepare_staticfiles()
    return deploy
