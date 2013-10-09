from ape import tasks

@tasks.register
@tasks.requires_product_environment
def collectstatic(force=False):
    """
    collect static files for production httpd

    If run with ``settings.DEBUG==True``, this is a no-op
    unless ``force`` is set to ``True``
    """
    #noise reduction: only collectstatic if not in debug mode
    from django.conf import settings
    if force or not settings.DEBUG:
        tasks.manage('collectstatic')
        print '... finished collectstatic'
        print
    else:
        print '... skipping collectstatic as settings.DEBUG=True; run ape collectstatic instead;'



def refine_deploy(original):
    """
    adds call to build_staticfiles
    """
    def deploy():
        original()
        tasks.collectstatic()
    return deploy
