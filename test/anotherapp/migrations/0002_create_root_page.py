from django.db import migrations


def create_root(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    Site = apps.get_model('wagtailcore.Site')
    HomePage = apps.get_model('anotherapp.HomePage')

    # Delete the default homepage
    # If migration is run multiple times, it may have already been deleted
    Page.objects.filter(id=2).delete()

    # Create content type for homepage model
    root_content_type, __ = ContentType.objects.get_or_create(
        model='homepage', app_label='anotherapp')

    # Create a new homepage
    root = HomePage.objects.create(
        title="Home",
        draft_title="Home",
        slug='home',
        content_type=root_content_type,
        path='00010001',
        depth=2,
        numchild=0,
        url_path='/home/',
    )

    # Create a site with the new homepage set as the root
    Site.objects.create(
        hostname='localhost', root_page=root, is_default_site=True)


def remove_root(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    HomePage = apps.get_model('anotherapp.HomePage')

    # Delete the default homepage
    # Page and Site objects CASCADE
    HomePage.objects.filter(slug='home', depth=2).delete()

    # Delete content type for homepage model
    ContentType.objects.filter(model='homepage', app_label='anotherapp').delete()


class Migration(migrations.Migration):

    run_before = [
        ('wagtailcore', '0053_locale_model'),
    ]

    dependencies = [
        ('anotherapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_root, remove_root),
    ]
