import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

User = get_user_model()


class EmailService:

    @staticmethod
    def send_email(data: dict):
        try:
            email = EmailMessage(
                subject=data.get('email_subject', ''),
                body=data.get('email_body', ''),
                to=[data.get('to_email', '')],
                from_email=settings.EMAIL_HOST_USER
            )
            email.send(fail_silently=False)
        except Exception as e:
            print(e)
            pass


class AccountService:

    @staticmethod
    def check_passwords_are_the_same(validated_data) -> bool:
        password = validated_data.get('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            return False
        return True
