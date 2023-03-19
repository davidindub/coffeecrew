import uuid


class set_guest_cookie_middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.COOKIES.get("guest_id"):
            guest_id = str(uuid.uuid4())
            response = self.get_response(request)
            response.set_cookie("guest_id", guest_id)
            return response

        return self.get_response(request)
