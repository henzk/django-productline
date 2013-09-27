import os
import sys

def main(args):
    
    if len(args) != 2:
        print 'install.py accepts exactly one argument <ape root dir>.'
        print 'The directory must not exist already.'
        sys.exit(1)
    
    webapps = args[1]
    webapps_dir = '%s/%s' % (os.getcwd(), webapps)
    
    cmds = (
        'wget -O - https://raw.github.com/henzk/ape/master/bin/bootstrape | python - %s ; ' % webapps + 
        'cd %s ; ' % webapps_dir +
        '. _ape/activape ; ' 
        'pip install -e git+https://github.com/henzk/django-productline#egg=django-productline ;'
    )
 
    os.system('bash -c "%s deactivape"; ' % cmds)
    # add initenv on ape container level
    initenv = open('%s/initenv' % webapps_dir, 'w+')
    initenv.write('export APE_PREPEND_FEATURES="ape.container_mode django_productline"')
    initenv.close()
    

if __name__ == '__main__':
    main(sys.argv)
