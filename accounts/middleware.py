from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

User = get_user_model()


class SetLastVisitMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if request.user.is_authenticated:
            User.objects.filter(pk=request.user.pk).update(last_visit=now())
        return response
