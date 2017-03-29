# coding: utf-8

import re
from six import iteritems

from django import template
from django.core.urlresolvers import resolve
from django.utils import translation

from modeltranslation.utils import get_language

register = template.Library()


# CHANGE LANGUAGE
@register.simple_tag(takes_context=True)
def translated_url(context, lang=None, *args, **kwargs):
    current_language = get_language()

    if 'request' in context and lang and current_language:
        request = context['request']
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

            # for a routable page, args[0] is the method with the @route
            # decorator, and args[2] the urlpaths captured by the regex in a
            # dict of form { key (variable name) : value (variable value) }

            if args:
                # so far I will just support one extra path step,
                # so len(args[2]) == 1
                # TODO: more flexible support
                # _suffix = '_slug'
                # for _key, _value in iteritems(args[2]):
                #     if _key.endswith(_suffix):
                #         key = _key[:len(_suffix)]
                #         value = _value
                _, value = next(iteritems(args[2]))
                snippet = page.SNIPPET_CLASS.objects.get(slug=value)
            with translation.override(lang):
                if args:
                    return page.url + snippet.slug + '/'
                else:
                    return page.url

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
