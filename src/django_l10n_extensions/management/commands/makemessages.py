# -*- coding: UTF-8 -*-
import logging
from argparse import RawTextHelpFormatter

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.commands import makemessages
from django.db.models import Model

from django_l10n_extensions.models.fields import TransField
from django_l10n_extensions.po_utils import update_messages

User = get_user_model()
log = logging.getLogger(__name__)


class Command(makemessages.Command):
    """
    Overwrite existing django makemigrations management command cause we want to force the LANGUAGE_CODE to 'en'
    """
    help = ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
            "!! Overwrites existing django makemessages management command \n"
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
            "!!\n"
            "!! It adds collection messages from the TransField field of the models\n"
            "!!\n"
            "\n"
            "" + makemessages.Command.help)

    def create_parser(self, *args, **kwargs):
        parser = super(Command, self).create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser

    def add_arguments(self, parser):
        parser.add_argument('--no-models', dest='no-models', action='store_true',
            help="Don't collect the TransField translation, that is makemessages will run as the original Django's makemessages command")
        parser.add_argument('--models-only', dest='models-only', action='store_true',
            help="Only collect the model messages, that is skips the default behaviour of Django's makemessages command.")
        super(Command, self).add_arguments(parser)

    def handle(self, *app_labels, **options):
        if not options['no-models']:
            self.collect_model_messages(options)
        return super(Command, self).handle(*app_labels, **options)

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


