


def get_context():
    '''
    Features which require configuration parameters in the product context need to refine
    this method and update the context with their own data.
    '''

    import random

    return {
        'SITE_ID':  1,
        'SECRET_KEY': ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)]),
    }
            
