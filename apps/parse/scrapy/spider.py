class InjectUrlMixin:
    def __init__(self, *args, **kwargs):
        url = kwargs.pop("url", None)
        if not getattr(self.__class__, "start_urls", None) and url:
            super().__init__(*args, start_urls=[url])
        else:
            super().__init__(*args, **kwargs)
