"""
This feature enables an optional multi-language admin.
Therefore, it refines the base implementation of the get_admin_urls function in djpladmin.
Obviously, djpladmin needs to be enabled, too and added before this feature.
It simply wraps the original implementation, which simply returns the include of the admin urls, into the i18n_patterns-function.
"""
