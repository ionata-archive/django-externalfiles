django-externalfiles
======================

Serve files sensibly through Django that do not live in the webroot.

This is great for serving private files. By routing through Django first, any
authentication checks can be run before serving the file.

Installing
----------

    pip install django-externalfiles

Setting up
----------

Add the following settings to your `settings.py`:

    EXTERNALFILES_UPLOAD_ROOT = '/path/to/external/files/'
    EXTERNALFILES_SERVER = 'externalfiles.servers.DebugFileServer'

`EXTERNALFILES_UPLOAD_ROOT` should be the absolute path to the location of the
external files you want to serve.

`EXTERNALFILES_SERVER` should be the full dotted python import path of an
`ExternalFileServer` class. `django-externalfiles` comes with four servers:

### `DebugFileServer`

This file server uses Django's in built static file server to work. As such, it
should **only** be used for development servers, and not for production
servers!

### `ApacheXSendfileServer`

This file server makes use of the [mod_xsendfile][] Apache module to send
files. To install `mod_xsendfile` on a Debian/Ubuntu system, run:

    # apt-get install libapache2-mod-xsendfile
    # a2enmod xsendfile

and put the following in the Django vhost:

    XSendFile On
    XSendFilePath /path/to/external/files

### `NginxXAccelServer`

This file server makes use of the [X-Accel][] module from Nginx to serve files.
Use this if your Django app lives behind an nginx server.

Using `NginxXAccelServer` required one extra setting:
`EXTERNALFILES_NGINX_URL_BASE`. This should be the base URL that Nginx serves
`X-Accel-Redirect` files from. For example, if your Nginx config contained the
following:

    location /protected_files {
            internal;
            alias /path/to/external/files;
    }

You would use the following in your settings:

    EXTERNALFILES_SERVER = 'externalfiles.servers.NginxXAccelServer'
    EXTERNALFILES_UPLOAD_ROOT = '/path/to/external/files'
    EXTERNALFILES_NGINX_URL_BASE = '/protected_files'

Using
-----

`django-externalfiles` is designed to be used as part of a view. The basic use
case is checking for permission based on user permissions before serving a
private file. It is also designed to work closely with FileFields on models.
Consider the following model:

    from django.db import models
    from externalfiles import storage_engine

    class PrivateAttachment(models.Model):

        user = models.ForeignKey('auth.User')
        file = models.FileField(upload_to='private_attachments/',
                                storage=storage_engine)

A users private file could be served using the following view:

    from .models import PrivateAttachment
    from externalfiles.views import serve

    def serve_attachment(request, attachment_pk):

        # Get an attachment for the current user, 404 otherwise
        attachment = get_object_or_404(PrivateAttachment,
                                       user=request.user,
                                       pk=attachment_pk)

        # Serve the file
        return serve(request, attachment.file)

The `PrivateAttachment.file` is a normal file field, but uses the
`externalfiles.storage_engine` to store its files. This storage engine is a
`django.core.files.storage.FileSystemStorage` with `location` set to
`settings.EXTERNALFILES_UPLOAD_ROOT`. You can continue to use normal forms for
file upload, and treat it just like a normal file field, with one exception:
you can not serve it via `file.url`.

[X-accel]: http://wiki.nginx.org/X-accel "X-accel on wiki.nginx.org"
[mod_xsendfile]: https://tn123.org/mod_xsendfile/ "mod_xsendfile for Apache2/Apache2.2"
