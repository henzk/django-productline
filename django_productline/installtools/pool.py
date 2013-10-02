import os


class FeaturePool(object):


    def __init__(self, pool_dir):
        self.pool_dir = pool_dir
        
        
    
    def get_path(self, rel_path):
        return os.path.join(self.pool_dir, rel_path)
