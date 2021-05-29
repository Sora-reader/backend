import easy
from django.utils.html import format_html


class AuthorLinkMixin:
    @easy.smart(short_description="Author", admin_order_field="author__name")
    def author_link(self, obj) -> str:
        return (
            format_html(f"<a href='{obj.author.get_admin_url()}'>{obj.author.name}</a>")
            if obj.author
            else "-"
        )


class ImagePreviewMixin:
    @easy.smart(__name__="Image")
    def get_image(self, obj):
        style = "max-height: 100px; border-radius: 3px;"
        return format_html(f"<img src='{obj.image_url}' style='{str(style)}' />")
