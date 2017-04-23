from django.utils.translation import pgettext, gettext, ngettext

def _reload(instance):
    """
    :param instance: a django model instance
    :return: a refreshed instance of the same django model instance
    """
    return type(instance).objects.get(pk=instance.pk)


def setup_translations():
    gettext('edit')
    pgettext('season', 'spring')
    pgettext('mechanical device', 'spring')
    gettext('"double quote"')
    gettext("'single quote'")
    gettext("'single quote' with escaped \"double\"")
    gettext('"double quote" with exceped \'single\'')
    count = 3
    ngettext("You bought {} apple", "You bought {} apples", count)