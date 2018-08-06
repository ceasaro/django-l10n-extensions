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
import pkg_resources
from django.templatetags import i18n

from django_l10n_extensions.po_utils import get_po_entry
from django_l10n_extensions.settings import use_inline_trans
from .utils import html_escape


def get_version(svn=False):
    """Returns the version as a human-format string."""
    v = pkg_resources.require("django_l10n_extensions")[0].version
    if svn:
        from django.utils.version import get_svn_revision
        import os
        svn_rev = get_svn_revision(os.path.dirname(__file__))
        if svn_rev:
            v = '%s-%s' % (v, svn_rev)
    return v


def to_html(msgid, value, html_tag='span'):
    po_entry, po_lib = get_po_entry(msgid)

    return u"<{html_tag} data-msgid='{msgid}' class='_itr {not_translated}'>{value}</{html_tag}>".format(
        msgid=html_escape(msgid),
        value=value,
        not_translated='not_translated' if not po_entry or not po_entry.translated() else '',
        html_tag=html_tag
    )


class InlineTranslateNode(i18n.TranslateNode):

    def render(self, context):
        splitted = self.token.split_contents()
        tag_name, msgid = splitted[0], splitted[1]
        value = super(InlineTranslateNode, self).render(context)
        return to_html(msgid[1:-1], value)  # [1:-1] to strip of first and last "-char


class InlineBlockTranslateNode(i18n.BlockTranslateNode):

    def render(self, context, nested=False):
        singular, vars = self.render_token_list(self.singular)
        value = super(InlineBlockTranslateNode, self).render(context, nested)
        return to_html(singular, value, html_tag='div')


if use_inline_trans():
    i18n.TranslateNode = InlineTranslateNode
    i18n.BlockTranslateNode = InlineBlockTranslateNode
