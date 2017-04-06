# -*- coding: utf-8 -*-
from __future__ import absolute_import

from modeltranslation.translator import register, \
    TranslationOptions as TranslationOptionsOrig

from modeltranslation_wagtail.translator import translator, \
    TranslationOptions

from .models import (
    TestRootPage, TestSlugPage1, TestSlugPage2, PatchTestPage,
    PatchTestSnippet, FieldPanelPage, ImageChooserPanelPage, FieldRowPanelPage,
    MultiFieldPanelPage, InlinePanelPage, FieldPanelSnippet,
    ImageChooserPanelSnippet, FieldRowPanelSnippet, MultiFieldPanelSnippet,
    PageInlineModel, BaseInlineModel, StreamFieldPanelPage,
    StreamFieldPanelSnippet, SnippetInlineModel, InlinePanelSnippet)


# ######### Wagtail Models

@register(TestRootPage)
class TestRootPagePageTranslationOptions(TranslationOptions):
    fields = ()


@register(TestSlugPage1)
class TestSlugPage1TranslationOptions(TranslationOptions):
    fields = ()


@register(TestSlugPage2)
class TestSlugPage2TranslationOptions(TranslationOptions):
    fields = ()


@register(PatchTestPage)
class PatchTestPageTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(PatchTestSnippet)
class PatchTestSnippetTranslationOptions(TranslationOptionsOrig):
    fields = ('name',)


# ######### Panel Patching Models

@register(FieldPanelPage)
class FieldPanelPageTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(FieldPanelSnippet)
class FieldPanelSnippetTranslationOptions(TranslationOptionsOrig):
    fields = ('name',)


@register(ImageChooserPanelPage)
class ImageChooserPanelPageTranslationOptions(TranslationOptions):
    fields = ('image',)


@register(ImageChooserPanelSnippet)
class ImageChooserPanelSnippetTranslationOptions(TranslationOptionsOrig):
    fields = ('image',)


@register(FieldRowPanelPage)
class FieldRowPanelPageTranslationOptions(TranslationOptions):
    fields = ('other_name',)


@register(FieldRowPanelSnippet)
class FieldRowPanelSnippetTranslationOptions(TranslationOptionsOrig):
    fields = ('other_name',)


@register(StreamFieldPanelPage)
class StreamFieldPanelPageTranslationOptions(TranslationOptions):
    fields = ('body',)


@register(StreamFieldPanelSnippet)
class StreamFieldPanelSnippetTranslationOptions(TranslationOptionsOrig):
    fields = ('body',)


# TODO: check out how translator.register works for this one

class MultiFieldPanelTranslationOptions(TranslationOptionsOrig):
    fields = ()


translator.register(MultiFieldPanelPage, MultiFieldPanelTranslationOptions)
translator.register(MultiFieldPanelSnippet,
                    MultiFieldPanelTranslationOptions)

# end TODO


@register(BaseInlineModel)
class BaseInlineModelTranslationOptions(TranslationOptionsOrig):
    fields = ('field_name', 'image_chooser', 'fieldrow_name',)


class InlinePanelTranslationOptions(TranslationOptionsOrig):
    fields = ()


translator.register(PageInlineModel, InlinePanelTranslationOptions)
translator.register(SnippetInlineModel, InlinePanelTranslationOptions)


@register(InlinePanelPage)
class InlinePanelPageModelTranslationOptions(TranslationOptions):
    fields = ()


@register(InlinePanelSnippet)
class InlinePanelSnippetModelTranslationOptions(TranslationOptionsOrig):
    fields = ()
