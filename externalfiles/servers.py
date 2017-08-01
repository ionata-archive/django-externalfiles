import mimetypes
import posixpath

from django.conf import settings
from django.http import HttpResponse
from django.views.static import serve


class ExternalFileServer(object):

    def serve(file):
        raise NotImplemented()


class DebugFileServer(ExternalFileServer):

    def serve(self, request, file_path):
        assert file_path.startswith(settings.EXTERNALFILES_UPLOAD_ROOT)

        return serve(request, file_path, document_root='/')


class NginxXAccelServer(ExternalFileServer):

    def serve(self, request, file_path):
        assert file_path.startswith(settings.EXTERNALFILES_UPLOAD_ROOT)

        path_from_root = file_path[len(settings.EXTERNALFILES_UPLOAD_ROOT):]
        url_base = settings.EXTERNALFILES_NGINX_URL_BASE
        x_accel_url = posixpath.join(url_base, path_from_root.lstrip(posixpath.sep))

        response = HttpResponse('')
        response['X-Accel-Redirect'] = x_accel_url

        return response


class XSendfileServer(ExternalFileServer):

    def serve(self, request, file_path):
        assert file_path.startswith(settings.EXTERNALFILES_UPLOAD_ROOT)

        mimetype, encoding = mimetypes.guess_type(file_path)
        mimetype = mimetype or 'application/octet-stream'
        response = HttpResponse('', mimetype=mimetype)
        response['X-Sendfile'] = file_path

        return response


class ApacheXSendfileServer(XSendfileServer):
    pass


class LighttpXSendfileServer(XSendfileServer):
    pass
