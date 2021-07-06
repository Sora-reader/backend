from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # UI
    path(
        "",
        TemplateView.as_view(
            template_name="swagger-ui.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc-ui.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="redoc-ui",
    ),
]
