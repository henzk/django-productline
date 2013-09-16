


def refine_INSTALLED_APPS(original):
    return ['{{ cookiecutter.feature_name }}'] + list(original)
