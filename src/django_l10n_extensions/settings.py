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
"""

You have to define an AUTO_RELOAD_METHOD in your settings or
DEFAULT_AUTO_RELOAD_METHOD will be used.

Options for this settings::
  * "test" for a django instance (this do a touch over settings.py for reload)
  * "apache2"
  * "httpd"
  * "wsgi"
  * "restart_script <script_path_name>"

"""
from django.core.exceptions import ImproperlyConfigured

DEFAULT_ENABLE_INLINE_TRANS = False
DEFAULT_AUTO_RELOAD_METHOD = 'test'
DEFAULT_AUTO_RELOAD_TIME = '5'
DEFAULT_AUTO_RELOAD_LOG = 'var/log/autoreload_last.log'
STARLETTE_L10N_STORE = 'starlette_l10n_store'


def use_starlette_context():
    from django.conf import settings
    try:
        return settings.L10N_STORE == STARLETTE_L10N_STORE
    except (ImproperlyConfigured, AttributeError):
        return False


def use_inline_trans():
    from django.conf import settings
    try:
        return settings.ENABLE_INLINE_TRANS
    except (ImproperlyConfigured, AttributeError):
        return DEFAULT_ENABLE_INLINE_TRANS


def user_can_update(user):
    return use_inline_trans() and user.is_staff


def get_auto_reload_method():
    from django.conf import settings
    try:
        return settings.AUTO_RELOAD_METHOD
    except (ImproperlyConfigured, AttributeError):
        return DEFAULT_AUTO_RELOAD_METHOD


def get_auto_reload_time():
    from django.conf import settings
    try:
        return settings.AUTO_RELOAD_TIME
    except (ImproperlyConfigured, AttributeError):
        return DEFAULT_AUTO_RELOAD_TIME


def get_auto_reload_log():
    from django.conf import settings
    try:
        return settings.AUTO_RELOAD_LOG
    except (ImproperlyConfigured, AttributeError):
        return DEFAULT_AUTO_RELOAD_LOG


def get_default_l10n():
    from django.conf import settings
    try:
        from django_l10n_extensions.models import L10n
        return L10n(**settings.DEFAULT_L10N_CONFIG)
    except (ImproperlyConfigured, AttributeError):
        from django_l10n_extensions.models.models import DEFAULT_L10N
        return DEFAULT_L10N
