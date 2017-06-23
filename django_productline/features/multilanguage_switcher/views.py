from django.core.urlresolvers import translate_url
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.translation import check_for_language
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.views.generic import View


class ChangeLangView(View):

    def get(self, *args, **kwargs):
        """
        This view is used for changing the language (i18n).
        :return:
        """
        from django.conf import settings
        new_lang = self.request.GET.get('lang')
        response = HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        translation.activate(new_lang)
        if new_lang and check_for_language(new_lang):
            next_trans = translate_url(self.request.META.get('HTTP_REFERER'), new_lang)
            response = HttpResponseRedirect(next_trans)
        if hasattr(self.request, 'session'):
            self.request.session[LANGUAGE_SESSION_KEY] = new_lang
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, new_lang,
                                max_age=settings.LANGUAGE_COOKIE_AGE,
                                path=settings.LANGUAGE_COOKIE_PATH,
                                domain=settings.LANGUAGE_COOKIE_DOMAIN)
        return response
