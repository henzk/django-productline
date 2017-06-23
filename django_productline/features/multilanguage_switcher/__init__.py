"""
This feature requires the multilanguage feature.

It adds language switching functionality to django productline.

To use the view, pass the language code as GET-parameter to the view::

    href="{% url 'activate_language' %}?lang={{ language.0 }}" # language.0 is the language code, language.1 the language name

Of course, the language has to be enabled in settings.LANGUAGES.
Therefore, at least the multilanguage feature is required.

To enable the switcher template, include it anywhere in your template structure.
The rendering of the language choices relies on djangos i18n-contextprocessor.
"""
