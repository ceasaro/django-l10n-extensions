from optparse import make_option

from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import Model

from django_l10n_extensions.models.fields import TransField
from django_l10n_extensions.po_utils import update_messages


class Command(BaseCommand):
    help = "Updates the po files for the TransField model fields. "
    option_list = BaseCommand.option_list + (
        make_option('-l', '--locale',
                    dest='locale',
                    help="Creates or updates the message files for the given locale(s) (e.g. pt_BR). "
                         "Can be used multiple times."),
    )

    def handle(self, *args, **options):
        # for the dutch language also update the translations, cause the database is leading for dutch translations
        locales = options['locale']
        if not locales:
            locales = [l[0] for l in settings.LANGUAGES]

        for subcls in Model.__subclasses__():
            trans_fields = [f for f in subcls._meta.fields if type(f) == TransField]
            if trans_fields:
                print ('gathering translations for model {}'.format(subcls))
                for trans_field in trans_fields:
                    t9n_list = subcls.objects.values_list(trans_field.name, flat=True)
                    for locale in locales:
                        update_messages(locale, t9n_list)
        #     try:
        #         values = values.exclude(deleted=True)
        #     except FieldError:
        #         print ("no deleted in model %s" % subcls)
        #     # we use the name field as the default dutch translation
        #     msg_data = [{'msgid': _tuple[0], 'msgstr': _tuple[1], 'msgctxt': _tuple[1]}
        #                 for _tuple in values.values_list('labelname', 'name')]
        #     update_i18n_model_po_file(lang, msg_data, update_translations=update_translations)
        #
        # # update subscription descriptions
        # for subscription in Subscription.objects.filter(public=True).exclude(description__isnull=True).exclude(description__exact=''):
        #     ctxt = 'subscription {}'.format(subscription.name)
        #     msg_data = [{'msgid': subscription.description, 'msgctxt': ctxt}]
        #     update_i18n_model_po_file(lang, msg_data, update_translations=False)
        #
        # # update the country names translations
        # countries = Country.objects.filter(dataset_enabled=True)
        # update_i18n_model_po_file_msg_ids(lang, [name[0] for name in countries.values_list('name')])