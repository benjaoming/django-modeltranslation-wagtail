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
                # TODO: more flexible support on urlpath args
                urlpaths_args = args[2]

                # _suffix = '_slug'
                # for _key, _value in iteritems(args[2]):
                #     if _key.endswith(_suffix):
                #         key = _key[:len(_suffix)]
                #         value = _value
                if urlpaths_args:
                    _, value = next(iteritems(args[2]))
                    snippet = page.snippet_model_cls().objects.get(slug=value)
                else:
                    # TODO: more flexible support on extra path components
                    extra_path_component = None
                    if len(path_components) == 1 and \
                       page.id == request.site.root_page.id:
                        # routing root '/', so root is a RoutablePageMixin,
                        # and path_components[0] is some pattern to be
                        # matched with one of root's @route methods
                        extra_path_component = path_components[0]
                    elif len(path_components) == 2:
                        # with our @route patterns, each page only matches one
                        # path component, so we here we are sure not routing
                        # root. We are actually routing a page plus an extra
                        # path component, so path_components[0] will be the
                        # page's url and path_components[1] the extra to be
                        # matched with one of the page's @route method.s
                        extra_path_component = path_components[1]

                    if extra_path_component:
                        # get the name of the @route method (language
                        # independent) so we can reverse patterns later in
                        # another language
                        subpage_view_name = page.resolve_subpage(
                            '/' + extra_path_component + '/')[0].__name__

            with translation.override(lang):
                if urlpaths_args:
                    # filter by category, pass slugs as args, captured in
                    # urlpaths_args
                    return page.url + snippet.slug + '/'
                elif extra_path_component:
                    # RoutablePageMixin with an extra path componnent, use the
                    # name of the view that we extracted in order to get the
                    # extra url component in the new language
                    return page.url + page.reverse_subpage(subpage_view_name)
                else:
                    # just return the page url
                    # TODO: more flexible support
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
