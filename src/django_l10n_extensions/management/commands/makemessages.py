# -*- coding: UTF-8 -*-
import logging
from argparse import RawTextHelpFormatter

from django.contrib.auth import get_user_model
from django.core.management.commands import makemessages

from django_l10n_extensions.management.commands.make_l10n_messages import Command as L10nCommand

User = get_user_model()
logger = logging.getLogger(__name__)


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
            help="Don't collect the TransField translation")
        super(Command, self).add_arguments(parser)

    def handle(self, *app_labels, **options):
        if not options['no-models']:
            L10nCommand().collect_model_messages(options)
        return super(Command, self).handle(*app_labels, **options)

