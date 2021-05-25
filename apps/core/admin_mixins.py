from django.utils.html import format_html


class AuthorLinkMixin:
    def author_link(self, obj) -> str:
        return (
            format_html(f"<a href='{obj.author.get_admin_url()}'>{obj.author.name}</a>")
            if obj.author
            else "-"
        )

    author_link.short_description = "Author"
    author_link.admin_order_field = "author__name"


class ImagePreviewMixin:
    def get_image(self, obj):
        return format_html("<img src='{}'  width='25' height='25' />".format(obj.image_url))

    get_image.__name__ = "Image"
