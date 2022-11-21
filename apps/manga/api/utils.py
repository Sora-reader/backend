def get_user_kw(request, prefix=""):
    return (
        {f"{prefix}user": request.user}
        if request.user.is_authenticated
        else {f"{prefix}session": request.session.session_key}
    )
