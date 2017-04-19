# Copyright (c) 2017 by Cees van Wieringen <ceesvw@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this programe.  If not, see <http://www.gnu.org/licenses/>.


from django.views.generic.base import View


from polib import POEntry

from django_l10n_extensions.mixins import JSONResponseMixin
from django_l10n_extensions.po_utils import get_po_entry
from django_l10n_extensions.settings import user_can_update


def po_entry_to_json(po_entry):
    if po_entry is None:
        return
    assert isinstance(po_entry, POEntry), "can only serialize POEntry instances, got a {} ({})".format(type(po_entry), po_entry)
    return {
            'msgid': po_entry.msgid,
            'msgctxt': po_entry.msgctxt if po_entry.msgctxt else '',
            'msgstr': po_entry.msgstr if po_entry.msgstr  else '',
            'flags': po_entry.flags,
            'translated': po_entry.translated()
        }


class PoEntryView(JSONResponseMixin, View):

    def get(self, request):
        msgid = request.GET.get('msgid')
        if msgid:
            po_entry, po_lib = get_po_entry(msgid)
            return self.render_to_response(context=po_entry_to_json(po_entry))


class PoEntryUpdateView(JSONResponseMixin, View):

    def post(self, request):
        result = {
            'updated': False
        }
        errors = []

        if not user_can_update(request.user):
            errors.append("you don't have sufficient rights to update translations.")
        else:
            msgid = request.POST.get('msgid')
            msgstr = request.POST.get('msgstr')
            if not msgid:
                errors.append("no msgid found can't update if no msgid provided")
            if not msgstr:
                errors.append("no translated msgstr found can't update with empty translation")
            if not errors:
                po_entry, po_lib = get_po_entry(msgid)
                if po_entry:
                    po_entry.msgstr = msgstr
                    result['updated'] = True
                    result['poentry'] = po_entry_to_json(po_entry)
                    po_lib.save()
                else:
                    errors.append("no translation message found for '{}', can't update unknown translation".format(msgid))
        result['errors'] = errors
        return self.render_to_response(context=result)


# def do_restart(request):
#     """
#     * "test" for a django instance (this do a touch over settings.py for reload)
#     * "apache"
#     * "httpd"
#     * "wsgi"
#     * "restart_script <script_path_name>"
#     """
#     if get_user_can_translate(request.user):
#         reload_method = get_auto_reload_method()
#         reload_log = get_auto_reload_log()
#         reload_time = get_auto_reload_time()
#         command = "echo no script"
#         if reload_method == 'test':
#             command = 'touch %s' % os.path.join(settings.BASEDIR, 'settings.py')
        ## No RedHAT or similars
        # elif reload_method == 'apache2':
        #     command = 'sudo apache2ctl restart'
        ## RedHAT, CentOS
        # elif reload_method == 'httpd':
        #     command = 'sudo service httpd restart'
        #
        # elif reload_method.startswith('restart_script'):
        #     command = ' '.join(reload_method.split(" ")[1:])
        # if os.path.exists(os.path.dirname(reload_log)):
        #     os.system("sleep 2 && %s &> %s & " % (command, reload_log))
        # else:
        #     print('The AUTO_RELOAD_LOG directory do not exist')  # Just in case our stdout is logged somewhere
        #     os.system("sleep 2 && %s & " % command)
        # return render_to_response('inlinetrans/response.html',
        #                           {'message': reload_time},
        #                           context_instance=RequestContext(request))

#    return HttpResponseRedirect(request.environ['HTTP_REFERER'])
