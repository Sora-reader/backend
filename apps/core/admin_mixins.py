from django.utils.html import format_html
import easy


class AuthorLinkMixin:



class ImagePreviewMixin:
    @easy.smart(__name__="Image")
    def get_image(self, obj):
        style = "max-height: 100px; border-radius: 3px;"
        return format_html(f"<img src='{obj.image_url}' style='{str(style)}' />")
