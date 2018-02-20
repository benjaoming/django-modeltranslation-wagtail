django-modeltranslation-wagtail
===============================

.. image:: https://readthedocs.org/projects/django-modeltranslation-wagtail/badge/?version=latest
   :target: http://django-modeltranslation-wagtail.readthedocs.io

.. image:: https://badge.fury.io/py/django-modeltranslation-wagtail.png
    :target: http://badge.fury.io/py/django-modeltranslation-wagtail

.. image:: https://travis-ci.org/benjaoming/django-modeltranslation-wagtail.png?branch=master
    :target: https://travis-ci.org/benjaoming/django-modeltranslation-wagtail


The glue between django-modeltranslation and wagtail


Features
--------

* Field-based translation for Wagtail using django-modeltranslation
* **TODO** Makes translated fields easily accessible to the Wagtail admin.
* Sensible to the currently activated language.


When to use this
----------------

Actually, you might not want to use this! Consider carefully to use
`wagtail-modeltranslation <https://github.com/infoportugal/wagtail-modeltranslation/>`__ as it has
substantially improved by not hard-copying ``django-modeltranslation`` anymore.
They are still pretty bad at responding to external contributions, though.

If you need to have 1:1 translation for Pages or Snippets in Wagtail, you could use django-modeltranslation.

Having another translation mechanism such as what `wagtailtrans <https://github.com/LUKKIEN/wagtailtrans>`__
describes as freeform trees is not a problem.

If you ONLY plan to use one kind of translation mechanism, you should also carefully consider
`wagtailtrans <https://github.com/LUKKIEN/wagtailtrans>`__. This project is really nice if you have already
used other approaches and want to mix both what wagtailtrans calls *freeform* and *synchronized* trees.


Background
----------

Originally, I was using `wagtail-modeltranslation <https://github.com/infoportugal/wagtail-modeltranslation/>`__.
The project has been sparsely maintained, but more seriously, it was monkey-patching Wagtail and using a hard-copy
of the modeltranslation codebase instead of a dependency reference to django-modeltranslation. The latter has
now been restored, which as lowered the motivation for this project.

This project introduces a bit of naming hell. But remember it like this: *django-modeltranslation-wagtail* has
wagtail at the end because it depends on *django-modeltranslation*, which depends on *django*.


Using django-modeltranslation or wagtail-modeltranslation?
----------------------------------------------------------

Switching is easy!

Since this project is directly based on django-modeltranslation, the creation of fields in the database and
django migrations remains the same. In case you are switching, just revisit your ``translation.py`` files
and change the imports to point to ``modeltranslation_wagtail``.
