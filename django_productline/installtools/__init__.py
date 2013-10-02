import os, sys, shutil, json
from subprocess import call, PIPE
from .venv import VirtualEnv
from .pool import FeaturePool 



def get_ape_venv():
    '''
    Returns the _ape virtualenv.
    '''
    return VirtualEnv(os.path.join(os.environ['APE_GLOBAL_DIR'], 'venv'))
    
    
def cleanup():
    '''
    Cleans up the installation directory.
    '''
    lib_dir = os.path.join(os.environ['CONTAINER_DIR'], '_lib')
    if os.path.exists(lib_dir):
        shutil.rmtree(lib_dir)
    os.mkdir(lib_dir)
    
    
def create_project_venv():
    '''
    Creates a project-level virtualenv and returns a ``VirtualEnv`` object.
    '''
    print '... creating project-level virtualenv'
    venv_dir = os.path.join(os.environ['CONTAINER_DIR'], '_lib/venv')
    
    if os.path.exists(venv_dir):
        print 'ERROR: virtualenv already exists!'
        sys.exit()
    
    try:
        call(['virtualenv', venv_dir, '--no-site-packages'])
    except OSError:
        print 'ERROR: You probably dont have virtualenv installed: sudo apt-get install python-virtualenv'
        sys.exit()
        
    print '... virtualenv successfully created'
    return VirtualEnv(venv_dir)


def fetch_pool(repo_url):
    '''
    Fetches a git repository from ``repo_url`` and returns a ``FeaturePool`` object.
    '''
    repo_name = repo_url.split('.git')[0].split('/')[-1]
    lib_dir = os.path.join(os.environ['CONTAINER_DIR'], '_lib')
    print '... fetching %s ' % repo_name
    
    if os.path.exists(os.path.join(lib_dir, repo_name)):
        print 'ERROR: repository already exists' 
        sys.exit()
        
    try:
        a = call(['git', 'clone', repo_url], cwd=lib_dir)
    except OSError:
        print 'ERROR: You probably dont have git installed: sudo apt-get install git'
        sys.exit()
    
    if a != 0:
        print 'ERROR: check your repository url and credentials!'
        sys.exit()
    
    print '... repository successfully cloned'
    return FeaturePool(os.path.join(lib_dir, repo_name))
    
        

def add_to_path(*args):
    print '... adding paths'
    paths = []
    for path in args:
        if type(path) == list:
            paths += path
        else:
            paths.append(path)
    
    target = os.path.join(os.environ['CONTAINER_DIR'], '_lib/paths.json')
    f = open(target, 'w')
    f.write(json.dumps(paths))
    f.close()
    print '... wrote paths.json'
    
    
    
    
    
    
    
    
