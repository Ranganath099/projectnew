# from user.models import CustomUser
# from django.contrib.auth.backends import BaseBackend

# class EmailOrPhoneBackend(BaseBackend):
#     def authenticate(self, request, identifier=None, password=None, **kwargs):
#         if not identifier or not password:  # Fix: Change username to identifier
#             return None

#         UserModel = CustomUser
#         try:
#             if "@" in identifier:  
#                 user = UserModel.objects.get(email=identifier)
#             else:
#                 user = UserModel.objects.get(phone_number=identifier)
#         except UserModel.DoesNotExist:
#             return None

#         if user and user.check_password(password):
#             return user
#         return None

from django.contrib.auth.backends import BaseBackend
from user.models import CustomUser

class EmailOrPhoneBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"Authenticating user: {username}")

        if not username or not password:
            print("Missing username or password")
            return None

        try:
            if "@" in username:
                user = CustomUser.objects.get(email__iexact=username)
            else:
                user = CustomUser.objects.get(phone_number=username)
        except CustomUser.DoesNotExist:
            print("User does not exist")
            return None

        if user.check_password(password):
            print("Authentication successful")
            return user
        
        print("Authentication failed")
        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
