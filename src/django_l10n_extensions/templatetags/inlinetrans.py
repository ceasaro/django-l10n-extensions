# Copyright (c) 2010-2013 by Yaco Sistemas <ant30tx@gmail.com> or <goinnn@gmail.com>
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

from django import template
from django.conf import settings
from django.urls import reverse

from django.utils.translation import get_language

from django_l10n_extensions import use_inline_trans


register = template.Library()


def get_static_url(subfix='inlinetrans'):
    static_prefix = getattr(settings, 'INLINETRANS_STATIC_URL', None)
    if static_prefix:
        return static_prefix
    static_prefix = getattr(settings, 'INLINETRANS_MEDIA_URL', None)
    if static_prefix:
        return static_prefix
    static_url = getattr(settings, 'STATIC_URL', getattr(settings, 'MEDIA_URL'))
    return '%s%s/' % (static_url, subfix)


def get_language_name(lang):
    for lang_code, lang_name in settings.LANGUAGES:
        if lang == lang_code:
            return lang_name


@register.inclusion_tag('inlinetrans/inline_header.html', takes_context=True)
def inlinetrans_static(context):
    tag_context = {
        'get_poentry_url': reverse('inlinetrans:get_po_entry'),
        'update_poentry_url': reverse('inlinetrans:update_poentry_url'),
        'can_translate': False,
        'INLINETRANS_STATIC_URL': get_static_url(),
        'INLINETRANS_MEDIA_URL': get_static_url(),  # backward compatible
        'request': context['request'],
    }
    user = context.get('user', None)
    if user and user.is_staff:
        tag_context.update({
            'can_translate': use_inline_trans,
            'is_staff': True,  # backward compatible
            'language': get_language_name(get_language()),
        })
    return tag_context




