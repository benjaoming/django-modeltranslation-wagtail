django-modeltranslation-wagtail
===============================

.. image:: https://readthedocs.org/projects/django-modeltranslation-wagtail/badge/?version=latest
    :target: http://django-modeltranslation-wagtail.readthedocs.io

.. image:: https://badge.fury.io/py/django-modeltranslation-wagtail.png
    :target: http://badge.fury.io/py/django-modeltranslation-wagtail

.. image:: https://circleci.com/gh/benjaoming/django-modeltranslation-wagtail.svg?style=shield
    :target: https://circleci.com/gh/benjaoming/django-modeltranslation-wagtail


Keep-it-simple glue between django-modeltranslation and Wagtail.


Features
--------

* Field-based translation for Wagtail using django-modeltranslation
* **TODO** Makes translated fields easily accessible to the Wagtail admin.
* Sensible to the currently activated language.
* The ``Page`` model isn't modified (no migrations added to Wagtail), translations of ``title``, ``seo_title`` and ``search_description`` are local to the translated models.


How to use
----------

You create Wagtail models and activate them with a ``<yourapp>.translation`` module, just like you would with any other modeltranslation-based model.

In Wagtail, it's the active language that decides what language you are editing in your translated model.

For instance, navigating to ``/en/wagtail/pages/add/<yourapp>/<yourmodel>/<ptr_id>/`` will create a new page in English.

Drawback: There is currently no UI for the translation workflow. This means that users have to *know* that they need to switch ``/en/`` with ``/fr/`` in the URL path after creating an English entry to edit it in French.


When to use this
----------------

Actually, you might not want to use this! Consider carefully to use
`wagtail-modeltranslation <https://github.com/infoportugal/wagtail-modeltranslation/>`__ as it has
substantially improved by not hard-copying ``django-modeltranslation`` anymore.

If you need to have 1:1 translation for Pages or Snippets in Wagtail, you could use django-modeltranslation.
However, ``wagtail-modeltranslation`` is a complex project that patches a lot of external code and therefore often breaks with the latest versions of Wagtail.

If you only need freeform translation (when pages in the page-tree aren't translated 1:1 but translations exist independently from one another), look no further than either Wagtail's built-in `simple_translation <https://docs.wagtail.io/en/latest/reference/contrib/simple_translation.html>`__ or `wagtail-localize <https://www.wagtail-localize.org/>`__. 


Background
----------

Originally, I was using `wagtail-modeltranslation <https://github.com/infoportugal/wagtail-modeltranslation/>`__.
The project has been sparsely maintained, but more seriously, it was monkey-patching Wagtail and using a hard-copy
of the modeltranslation codebase instead of a dependency reference to django-modeltranslation. The latter has
now been restored, which as lowered the motivation for this project.

A few years later, I returned to use wagtail-modeltranslation but once again found myself spending way too much time understanding non-merged PRs etc. To be fair, the project has been maintained in the meantime, but it was lacking behind and I couldn't figure out what to do to use it with the latest version of Wagtail.

This project introduces a bit of naming hell. But remember it like this: *django-modeltranslation-wagtail* has
wagtail at the end because it depends on *django-modeltranslation*, which depends on *django*.


Using django-modeltranslation or wagtail-modeltranslation?
----------------------------------------------------------

Switching is easy!

Since this project is directly based on django-modeltranslation, the creation of fields in the database and
django migrations remains the same. In case you are switching, just revisit your ``translation.py`` files
and change the imports to point to ``modeltranslation_wagtail``.
