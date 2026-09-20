from user.models import User

class AutoLoginMiddleware:
    """
    Ensures the user never has to manually log in or create an account.
    Automatically binds the primary active user to the request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # Auto-login as the primary active user (e.g. gocoupon13@gmail.com or admin)
            default_user = User.objects.filter(is_active=True).first()
            if default_user:
                request.user = default_user
        return self.get_response(request)
