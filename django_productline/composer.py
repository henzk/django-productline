import featuremonkey
from featuremonkey import helpers

class Composer(featuremonkey.Composer):
    """
    The django_productline composer is based on
    featuremonkey and adds a new composition rule
    that is useful for django product lines.

    Django makes extensive use of metaprogramming to
    provide the db.models, forms etc.
    Unfortunately, this renders the introduction mechanism of
    featuremonkey useless in some cases, e.g. when trying
    to introduce new fields in a django model.

    However, django provides the ``contribute_to_class`` hook
    that can be used to circumvent such problems in some cases.

    Therefore, this composer additionally provides a ``contribute``
    operation, that works a lot like ``introduce`` but uses
    ``contribute_to_class`` instead of ``setattr`` underneath.

    Contributions may not be specified as factory functions.
    Use explicit attribute assignment.
    """

    def _contribute(self, role, target_attrname, transformation, base):
        if hasattr(base, target_attrname):
            raise featuremonkey.CompositionError(
                'Cannot contribute "%s" of "%s" to "%s"!'
                ' Attribute exists already!' % (
                    target_attrname,
                    helpers._get_role_name(role),
                    helpers._get_base_name(base),
                )
            )
        if callable(transformation):
            raise featuremonkey.CompositionError(
                'Cannot contribute "%s" of "%s" to "%s"!'
                ' Contributions must not be callable!' % (
                    target_attrname,
                    helpers._get_role_name(role),
                    helpers._get_base_name(base),
                )
            )

        transformation.contribute_to_class(base, target_attrname)

    def _apply_transformation(self, role, base, transformation, attrname):
        if attrname.startswith('contribute_'):
            target_attrname = attrname[len('contribute_'):]
            self._contribute(role, target_attrname, transformation, base)
        else:
            super(Composer, self)._apply_transformation(
                role, base, transformation, attrname
            )

def get_composer():
    return Composer()
