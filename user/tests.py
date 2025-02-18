from django.test import TestCase

# Create your tests here.
# <--- past Login view --->

# User = get_user_model()  # Ensure we use the custom user model

# def user_login(request):
#     if request.method == "POST":
#         form = EmailOrPhoneLoginForm(request.POST)
#         if form.is_valid():
#             identifier = form.cleaned_data["identifier"]
#             password = form.cleaned_data["password"]
#             user = authenticate(request, username=identifier, password=password)  # Use username instead of identifier

#             if user is not None:
#                 if user.is_superuser:
#                     # Login superuser with both backends
#                     login(request, user, backend="django.contrib.auth.backends.ModelBackend")
#                 else:
#                     # Login regular users with custom backend
#                     login(request, user, backend="user.backends.EmailOrPhoneBackend")

#                 return redirect("/user/home/")  # Redirect all users to user home page
#             else:
#                 form.add_error(None, "Invalid email/phone number or password")
#     else:
#         form = EmailOrPhoneLoginForm()
    
#     return render(request, "login.html", {"form": form})

# @login_required(login_url="/user/login")
# def user_home(request):
#     return render(request, "user/home.html")

# <--- past backends.py --->
# for this superuser is login in home and backend admin but 
# class EmailOrPhoneBackend(BaseBackend):
#     def authenticate(self, request, identifier=None, password=None, **kwargs):
#         print(f"Authenticating with identifier: {identifier}, password: {password}")
#         if not identifier or not password:
#             return None

#         UserModel = CustomUser
#         try:
#             if "@" in identifier:
#                 user = UserModel.objects.get(email__iexact=identifier)
#             else:
#                 user = UserModel.objects.get(phone_number=identifier)
#         except UserModel.DoesNotExist:
#             print("User does not exist")
#             return None

#         if user and user.check_password(password):
#             print("Authentication successful")
#             return user

#         print("Authentication failed")
#         return None
