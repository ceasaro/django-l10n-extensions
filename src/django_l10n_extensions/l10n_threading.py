import threading
from copy import deepcopy


_local = threading.local()


def merge_l10n(l10n, l10n_to_merge):
    for key, value in l10n_to_merge.__dict__.items():
        if value:
            l10n.__dict__.update({key: value})


def get_l10n():
    """
    :return: active l10n. First look in local thread if not present check user localization
    """
    local_l10n = getattr(_local, "l10n_instance", None)
    if local_l10n:
        return local_l10n

    from django_l10n_extensions.models.models import DEFAULT_L10N
    l10n = deepcopy(DEFAULT_L10N)
    return l10n


def activate(l10n):
    if not l10n:
        return
    _local.l10n_instance = l10n


def deactivate():
    if hasattr(_local, "l10n_instance"):
        del _local.l10n_instance
