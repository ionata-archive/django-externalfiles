from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.files import File
from externalfiles import get_server

def serve(request, file_path):

    # Convert the argument into a file path
    if isinstance(file_path, (file, File)):
        file_path = file_path.path

    if not file_path.startswith(settings.EXTERNALFILES_UPLOAD_ROOT):
        raise SuspiciousOperation(
            "Attempted to serve file outside of EXTERNALFILES_UPLOAD_ROOT")

    server = get_server()
    return server.serve(request, file_path)
