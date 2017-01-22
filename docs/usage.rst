========
Usage
========

To use django-modeltranslation-wagtail in ``myapp.translation`` ::

    from modeltranslation.translator import register
	from modeltranslation_wagtail.translator import TranslationOptions
	
	from myapp.models import MyModel

    @register(MyModel)
    class MyModelTranslation(TranslationOptions):
        fields = (
            'content',
        )
