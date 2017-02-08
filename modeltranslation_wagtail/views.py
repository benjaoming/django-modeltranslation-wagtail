import re
from six import iteritems

from django.core.urlresolvers import resolve
from django.utils.translation import activate, get_language


def change_lang(request, page_slug, lang):
    current_language = get_language()

    if lang and current_language:
        match = resolve(request.path)
        non_prefixed_path = re.sub(
            current_language + '/', '', request.path, count=1)

        # means that is an wagtail page object
        if match.url_name == 'wagtail_serve':
            path_components = [
                component for component in non_prefixed_path.split('/')
                if component]
            page, args, kwargs = request.site.root_page.specific.route(
                request, path_components)

            activate(lang)
            translated_url = page.url
            raise ValueError('')
            activate(current_language)

            return translated_url
        elif match.url_name == 'wagtailsearch_search':
            path_components = [
                component for component in non_prefixed_path.split('/')
                if component]

            translated_url = '/' + lang + '/' + path_components[0] + '/'
            if request.GET:
                translated_url += '?'
                for key, value in iteritems(request.GET):
                    translated_url += key + '=' + value
            return translated_url

    return ''
