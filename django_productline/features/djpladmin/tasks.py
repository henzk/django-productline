from __future__ import unicode_literals, print_function
from ape import tasks
from operator import __or__ as OR


@tasks.register
@tasks.requires_product_environment
def sync_auth_groups():
    '''
    Syncs auth groups according to settings.AUTH_GROUPS
    '''
    from django.conf import settings
    from django.contrib.auth.models import Group, Permission
    from django.db.models import Q

    for data in settings.AUTH_GROUPS:
        g1 = Group.objects.get_or_create(name=data['name'])[0]
        g1.permissions.clear()
        g1.save()
        args = []
        print('*** Created group %s' % g1.name)
        for perm in data['permissions']:
            print(perm)
            args.append(Q(codename=perm[0], content_type__app_label=perm[1]))
            print('   *** Created permission %s' % perm[0])

        g1.permissions.add(*list(Permission.objects.filter(
            reduce(OR, args)
        )))


def refine_prepare_data(original):
    """
    Refines prepare data and creates potential superusers.
    :param original:
    :return:
    """

    def prepare_data():
        original()
        tasks.createsuperusers()

    return prepare_data


@tasks.register
@tasks.requires_product_environment
def createsuperusers():
    """
    Creates all superusers defined in settings.INITIAL_SUPERUSERS.
    These superusers do not have any circles. They are plain superusers.
    However you may want to signup yourself and make this new user a super user then.
    """
    from django.contrib.auth import models as auth_models
    from django.conf import settings
    from django.core.mail import send_mail
    from django.contrib.sites import models as site_models
    import uuid
    from django.db import transaction
    from django.db.models import Q

    site = site_models.Site.objects.get(id=settings.SITE_ID)

    for entry in settings.INITIAL_SUPERUSERS:
        # create initial supersuers.

        print('*** Create specified superuser {}'.format(entry['username']))

        if not auth_models.User.objects.filter(Q(username__in=[entry['username'], entry['email']]) | Q(email=entry['email'])).exists():
            # create the superuser if it does not exist yet
            with transaction.atomic():
                password = ''.join(str(uuid.uuid4())[:8])

                root = auth_models.User()
                root.first_name = entry.get('first_name', '')
                root.last_name = entry.get('last_name', '')
                root.email = entry['email']
                root.username = entry['username']
                root.set_password(password)
                root.is_active = True
                root.save()
                # overwrite default is_staff
                root.is_staff = True
                root.is_superuser = True
                root.save()

                send_mail(
                    subject='Your superuser account',
                    recipient_list=[entry['email']],
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    message='username: {username}\npassword: {pw}\nsite: {site}'.format(
                        username=root.username,
                        pw=password,
                        site=site.domain
                    ),
                )

                print('\tA new superuser was created. Check {}'.format(entry['email']))
        else:
            print('\tSpecified superuser already exists')
