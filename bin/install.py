import os
import sys

def main(args):

    if '--dev' in args:
        use_devel_version = True
        ape_devel_arg = '--dev'
        args.remove('--dev')
        djpl_install = 'pip install -e git+https://github.com/henzk/django-productline#egg=django-productline'
    else:
        use_devel_version = False
        ape_devel_arg = ''
        djpl_install = 'pip install django-productline'

    if len(args) != 2:
        print 'Usage:'
        print
        print 'install.py [--dev] <APE_ROOT_DIR>'
        print
        print 'Creates an ape-root at APE_ROOT_DIR for your django product lines.'
        print 'The given directory must not exist already.'
        print
        print 'If --dev is given, this installs the latest development versions from git.'
        print 'Otherwise, the latest stable version of ape and django-productline are used from PYPI.'
        sys.exit(1)

    webapps = args[1]
    webapps_dir = '%s/%s' % (os.getcwd(), webapps)

    cmds = (
        'wget -O - https://raw.github.com/henzk/ape/master/bin/bootstrape | python - %s %s; ' % (webapps, ape_devel_arg) + 
        'cd %s ; ' % webapps_dir +
        '. _ape/activape ; ' +
        djpl_install + '; '
    )

    os.system('bash -c "%s deactivape"; ' % cmds)
    # add initenv on ape container level
    with open('%s/initenv' % webapps_dir, 'w+') as initenv:
        initenv.write('export APE_PREPEND_FEATURES="ape.container_mode django_productline"')


if __name__ == '__main__':
    main(sys.argv)
