from optparse import make_option

import logging
from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import Model

from django_l10n_extensions.models.fields import TransField
from django_l10n_extensions.po_utils import update_messages

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Updates the po files for the TransField model fields. "
    option_list = BaseCommand.option_list + (
        make_option('-l', '--locale', default=[], dest='locale', action='append',
                    help="Creates or updates the message files for the given locale(s) (e.g. pt_BR). "
                         "Can be used multiple times."),
    )

    def handle(self, *args, **options):
        self.collect_model_messages(options)

    def collect_model_messages(self, options):
        # for the dutch language also update the translations, cause the database is leading for dutch translations
        locales = options['locale']
        if not locales:
            locales = [l[0] for l in settings.LANGUAGES]
        self.stdout.write("gathering django-l10n model translations for locales {}".format(locales))

        for subcls in Model.__subclasses__():
            if subcls.__module__ != '__fake__':
                trans_fields = [f for f in subcls._meta.fields if type(f) == TransField]

                if trans_fields:
                    log.debug('gathering translations for model {}'.format(subcls))
                    for trans_field in trans_fields:
                        t9n_list = [msg for msg in subcls.objects.values_list(trans_field.name, flat=True) if msg]
                        for locale in locales:
                            update_messages(locale, t9n_list)
