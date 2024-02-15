import threading
from copy import deepcopy

from django_l10n_extensions import settings

_local = threading.local()


def get_l10n():
    """
    :return: active l10n. First look in local thread if not present check user localization
    """
    local_l10n = None
    if settings.use_starlette_context():
        from starlette_context import context
        from starlette_context.errors import ContextDoesNotExistError

        try:
            local_l10n = context.get("l10n_instance")
        except ContextDoesNotExistError:
            pass
    if not local_l10n:
        local_l10n = getattr(_local, "l10n_instance", None)
    if local_l10n:
        return local_l10n

    l10n = deepcopy(settings.get_default_l10n())
    return l10n


def activate(l10n):
    if not l10n:
        return
    _local.l10n_instance = l10n


def deactivate():
    if hasattr(_local, "l10n_instance"):
        del _local.l10n_instance
