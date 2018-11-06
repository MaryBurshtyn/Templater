from os import path, environ, pathsep
from imgkit import from_file
from django.conf import settings


def make_thumbnail_save_path(html_document_path):
    return path.join(
        path.dirname(html_document_path),
        path.basename(html_document_path).replace(
            '.html',
            settings.THUMBNAIL_POSTFIX + '.' + settings.THUMBNAIL_EXTENSION
        )
    )


def create_thumbnail(html_document_path, thumbnail_save_path=None):
    if thumbnail_save_path is None:
        thumbnail_save_path = make_thumbnail_save_path(html_document_path)
    options = {
        'format': settings.THUMBNAIL_EXTENSION,
        'crop-w': '1920',
        'crop-h': '1080',
        'width': '1920',
        'height': '1080',
        'quiet': '',
        'quality': '50'
    }
    try:
        from_file(html_document_path, thumbnail_save_path, options=options)
    except OSError:
        if environ.get('PATH').find(settings.WKHTMLTOIMAGE_EXECUTABLE_PATH) != -1:
            raise
        environ.update({'PATH': environ.get('PATH') + pathsep + settings.WKHTMLTOIMAGE_EXECUTABLE_PATH})
        from_file(html_document_path, thumbnail_save_path, options=options)
    return thumbnail_save_path
