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


class PatchTestSnippetTranslationOptionsOrig(TranslationOptionsOrig):
    fields = ('name',)


translator.register(PatchTestSnippet, PatchTestSnippetTranslationOptionsOrig)


# ######### Panel Patching Models

class FieldPanelTranslationOptions(TranslationOptions):
    fields = ('name',)


class FieldPanelTranslationOptionsOrig(TranslationOptionsOrig):
    fields = ('name',)


translator.register(FieldPanelPage, FieldPanelTranslationOptions)
translator.register(FieldPanelSnippet, FieldPanelTranslationOptionsOrig)


class ImageChooserPanelTranslationOptions(TranslationOptions):
    fields = ('image',)


class ImageChooserPanelTranslationOptionsOrig(TranslationOptionsOrig):
    fields = ('image',)

translator.register(ImageChooserPanelPage, ImageChooserPanelTranslationOptions)
translator.register(ImageChooserPanelSnippet,
                    ImageChooserPanelTranslationOptionsOrig)


class FieldRowPanelTranslationOptions(TranslationOptions):
    fields = ('other_name',)


class FieldRowPanelTranslationOptionsOrig(TranslationOptionsOrig):
    fields = ('other_name',)


translator.register(FieldRowPanelPage, FieldRowPanelTranslationOptions)
translator.register(FieldRowPanelSnippet, FieldRowPanelTranslationOptionsOrig)


class StreamFieldPanelTranslationOptions(TranslationOptions):
    fields = ('body',)


class StreamFieldPanelTranslationOptionsOrig(TranslationOptionsOrig):
    fields = ('body',)


translator.register(StreamFieldPanelPage, StreamFieldPanelTranslationOptions)
translator.register(StreamFieldPanelSnippet,
                    StreamFieldPanelTranslationOptionsOrig)


class MultiFieldPanelTranslationOptions(TranslationOptions):
    fields = ()


class MultiFieldPanelTranslationOptionsOrig(TranslationOptionsOrig):
    fields = ()


translator.register(MultiFieldPanelPage, MultiFieldPanelTranslationOptions)
translator.register(MultiFieldPanelSnippet,
                    MultiFieldPanelTranslationOptionsOrig)


class BaseInlinePanelTranslationOptionsOrig(TranslationOptionsOrig):
    fields = ('field_name', 'image_chooser', 'fieldrow_name',)


translator.register(BaseInlineModel, BaseInlinePanelTranslationOptionsOrig)


class InlinePanelTranslationOptionsOrig(TranslationOptionsOrig):
    fields = ()


translator.register(PageInlineModel, InlinePanelTranslationOptionsOrig)
translator.register(SnippetInlineModel, InlinePanelTranslationOptionsOrig)


@register(InlinePanelPage)
class InlinePanelModelTranslationOptionsOrig(TranslationOptionsOrig):
    fields = ()


translator.register(InlinePanelSnippet, InlinePanelModelTranslationOptionsOrig)
