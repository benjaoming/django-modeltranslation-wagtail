========
Usage
========

In your Django settings, you need to add the following ::

    INSTALLED_APPS = [
        # ...
        "modeltranslation",
        "modeltranslation_wagtail",
    ]

To use django-modeltranslation-wagtail in ``myapp.translation`` ::

    from modeltranslation.translator import register
	from modeltranslation_wagtail.translator import TranslationOptions
	
	from myapp.models import MyModel

    @register(MyModel)
    class MyModelTranslation(TranslationOptions):
        fields = (
            'content',
        )
