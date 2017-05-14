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
import os

import polib

import sys

import re
from django.conf import settings
from django.utils.translation import get_language


def clean_po_entry(po_entry):
    if 'fuzzy' in po_entry.flags:
        po_entry.flags.remove('fuzzy')


po_libs = {}


def get_po_libs(locale):
    if locale in po_libs:
        return po_libs[locale]
    po_libs[locale] = []
    for _po_file in find_pos(locale=locale):
        po_libs[locale].append(polib.pofile(_po_file))
    return po_libs[locale]


def get_ordered_path_list(include_djangos):
    paths = []

    # settings
    for localepath in settings.LOCALE_PATHS:
        if os.path.isdir(localepath):
            paths.append(localepath)

    # project/locale
    parts = settings.SETTINGS_MODULE.split('.')
    project = __import__(parts[0], {}, {}, [])
    projectpath = os.path.join(os.path.dirname(project.__file__), 'locale')
    localepaths = [os.path.normpath(path) for path in settings.LOCALE_PATHS]
    if (projectpath and os.path.isdir(projectpath) and
        os.path.normpath(projectpath) not in localepaths):
        paths.append(os.path.join(os.path.dirname(project.__file__), 'locale'))

    # project/app/locale
    for appname in settings.INSTALLED_APPS:
        appname = str(appname)  # to avoid a fail in __import__ sentence
        p = appname.rfind('.')
        if p >= 0:
            app = getattr(__import__(appname[:p], {}, {}, [appname[p + 1:]]), appname[p + 1:])
        else:
            app = __import__(appname, {}, {}, [])

        apppath = os.path.join(os.path.dirname(app.__file__), 'locale')

        if os.path.isdir(apppath):
            paths.append(apppath)

    # django/locale
    if include_djangos:
        paths.append(os.path.join(os.path.dirname(sys.modules[settings.__module__].__file__), 'locale'))

    return paths


def find_pos(locale, include_djangos=False):
    """
    scans a couple possible repositories of gettext catalogs for the given
    language code

    """
    paths = get_ordered_path_list(include_djangos)

    ret = []
    rx = re.compile(r'(\w+)/../\1')
    langs = (locale, )
    if u'-' in locale:
        _l, _c = map(lambda x: x.lower(), locale.split(u'-'))
        langs += (u'%s_%s' % (_l, _c), u'%s_%s' % (_l, _c.upper()), )
    elif u'_' in locale:
        _l, _c = map(lambda x: x.lower(), locale.split(u'_'))
        langs += (u'%s-%s' % (_l, _c), u'%s-%s' % (_l, _c.upper()), )

    for path in paths:
        for lang_ in langs:
            dirname = rx.sub(r'\1', '%s/%s/LC_MESSAGES/' % (path, lang_))
            for fn in ('django.po', 'djangojs.po', ):
                if os.path.isfile(dirname + fn) and os.path.abspath((dirname + fn)) not in ret:
                    ret.append(os.path.abspath(dirname + fn))
    return ret


def get_po_entry(msg_id, po_file=None):
    locale = get_language()
    if not po_file:
        for po_lib in get_po_libs(locale):
            po_entry = po_lib.find(msg_id)
            if po_entry:
                return po_entry, po_lib
    else:
        po_lib = polib.pofile(po_file)
        return po_lib.find(msg_id), po_lib
    return None, None


def update_po_file(po_lib, t9n_list=None):
    if t9n_list:
        for t9n in t9n_list:
            msgid = t9n.msgid
            msgctxt = t9n.msgctxt
            msgid_plural = t9n.plural

            po_entry = None
            if msgid:
                if msgctxt:
                    po_entry = po_lib.find(msgid, msgctxt=msgctxt)
                if not msgctxt and not po_entry:
                    # search for poentry with only a msgid if no msgctxt is available
                    po_entry = po_lib.find(msgid)

                if not po_entry:
                    # no po entry found create a new one.
                    po_entry = polib.POEntry(msgid=msgid, msgctxt=msgctxt, msgid_plural=msgid_plural)
                    po_lib.append(po_entry)

        po_lib.save()


def update_messages(locale, t9n_list=None):
    libs = get_po_libs(locale)
    if libs:
        update_po_file(libs[0], t9n_list=t9n_list)  # update first found po lib