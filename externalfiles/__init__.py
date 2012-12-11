from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from django.utils.importlib import import_module


def load_server(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured(
            'Error importing external file server {0}: "{1}"'.format(path, e))
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(
            'Module "{0}" does not define a "{1}" external file server'.format(
                module, attr))

    return cls()


def get_server():
    try:
        server_path = settings.EXTERNALFILES_SERVER
        return load_server(server_path)
    except AttributeError:
        raise ImproperlyConfigured('No external file server has been defined. '
            'Does EXTERNALFILES_SERVER contain anything?')

storage_engine = FileSystemStorage(
    location=settings.EXTERNALFILES_UPLOAD_ROOT, base_url='/')
