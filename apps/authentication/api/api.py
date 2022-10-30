from django.contrib.auth import authenticate, login
from ninja import Router

from apps.authentication.api.schemas import CredentialsIn, SessionOut
from apps.core.api.schemas import ErrorSchema
from apps.core.api.utils import sora_schema

router = Router(tags=["Auth"])


@router.post("/login/", response=sora_schema(SessionOut))
def login_view(request, credentials: CredentialsIn):
    user = authenticate(request, username=credentials.username, password=credentials.password)
    if user is not None:
        login(request, user)
        return 200, SessionOut(session=request.session.session_key)
    else:
        return 400, ErrorSchema(error="Неверный логин или пароль")
